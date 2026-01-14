import torch
import torch.nn as nn
from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer
)
from datasets import load_dataset, Audio, DatasetDict
import evaluate
from dataclasses import dataclass
from typing import Any, Dict, List, Union

# 1. Configuration & Constants
MODEL_NAME = "openai/whisper-large-v3"
LANGUAGE = "Thai"
TASK = "transcribe"

class WhisperFinetuner:
    def __init__(self, model_id: str):
        self.processor = WhisperProcessor.from_pretrained(model_id, language=LANGUAGE, task=TASK)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_id)
        self.metric = evaluate.load("wer")

    def prepare_dataset(self, batch):
        # Process audio to 16kHz
        audio = batch["audio"]
        batch["input_features"] = self.processor.feature_extractor(
            audio["array"], sampling_rate=audio["sampling_rate"]
        ).input_features[0]

        # Tokenize Thai transcript with specific normalization for Thai scripts
        batch["labels"] = self.processor.tokenizer(batch["sentence"]).input_ids
        return batch

    def compute_metrics(self, pred):
        pred_ids = pred.predictions
        label_ids = pred.label_ids
        label_ids[label_ids == -100] = self.processor.tokenizer.pad_token_id

        pred_str = self.processor.tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
        label_str = self.processor.tokenizer.batch_decode(label_ids, skip_special_tokens=True)

        wer = 100 * self.metric.compute(predictions=pred_str, references=label_str)
        return {"wer": wer}

@dataclass
class DataCollatorSpeechSeq2SeqWithPadding:
    processor: Any

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        input_features = [{"input_features": feature["input_features"]} for feature in features]
        batch = self.processor.feature_extractor.pad(input_features, return_tensors="pt")

        label_features = [{"input_ids": feature["labels"]} for feature in features]
        labels_batch = self.processor.tokenizer.pad(label_features, return_tensors="pt")

        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)
        batch["labels"] = labels
        return batch

def train():
    finetuner = WhisperFinetuner(MODEL_NAME)
    
    # Loading Thai Common Voice + Custom "Thanglish" Creator dataset
    # Note: Replace with actual private dataset paths for production
    ds = load_dataset("mozilla-foundation/common_voice_11_0", "th", split="train+validation", trust_remote_code=True)
    ds = ds.cast_column("audio", Audio(sampling_rate=16000))
    ds = ds.map(finetuner.prepare_dataset, remove_columns=ds.column_names, num_proc=4)

    data_collator = DataCollatorSpeechSeq2SeqWithPadding(processor=finetuner.processor)

    training_args = Seq2SeqTrainingArguments(
        output_dir="./whisper-v3-thai-creator",
        per_device_train_batch_size=8,
        gradient_accumulation_steps=2,
        learning_rate=1e-5,
        warmup_steps=500,
        max_steps=5000,
        gradient_checkpointing=True,
        fp16=True,
        evaluation_strategy="steps",
        per_device_eval_batch_size=8,
        predict_with_generate=True,
        generation_max_length=225,
        save_steps=1000,
        eval_steps=1000,
        logging_steps=25,
        report_to=["tensorboard"],
        load_best_model_at_end=True,
        metric_for_best_model="wer",
        greater_is_better=False,
        push_to_hub=False,
    )

    trainer = Seq2SeqTrainer(
        args=training_args,
        model=finetuner.model,
        train_dataset=ds,
        data_collator=data_collator,
        compute_metrics=finetuner.compute_metrics,
        tokenizer=finetuner.processor.feature_extractor,
    )

    trainer.train()

if __name__ == "__main__":
    train()