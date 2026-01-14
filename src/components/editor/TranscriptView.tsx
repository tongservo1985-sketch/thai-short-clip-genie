"use client";

import React from 'react';
import { useEditorStore } from '@/store/useEditorStore';
import { clsx } from 'clsx';
import { Search, Scissors } from 'lucide-react';

export default function TranscriptView() {
  const { transcript, currentTime, setCurrentTime } = useEditorStore();

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-slate-800 flex items-center justify-between">
        <h2 className="font-semibold text-sm uppercase tracking-wider text-slate-400">
          Thai Transcript (AI)
        </h2>
        <div className="flex gap-2">
          <button className="p-1.5 hover:bg-slate-800 rounded-md transition">
            <Search size={16} />
          </button>
          <button className="p-1.5 hover:bg-slate-800 rounded-md transition">
            <Scissors size={16} />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 leading-relaxed">
        <div className="flex flex-wrap gap-x-1.5 gap-y-2">
          {transcript.map((word, index) => {
            const isActive = currentTime >= word.start && currentTime <= word.end;
            
            return (
              <span
                key={index}
                onClick={() => setCurrentTime(word.start)}
                className={clsx(
                  "cursor-pointer px-1 rounded transition-all duration-200 text-lg",
                  isActive 
                    ? "bg-brand-primary text-white scale-105 shadow-lg shadow-brand-primary/20" 
                    : "text-slate-300 hover:bg-slate-800"
                )}
              >
                {word.text}
              </span>
            );
          })}
        </div>
      </div>
      
      <div className="p-4 bg-slate-800/30 text-[10px] text-slate-500 italic">
        *คลิกที่คำเพื่อเลื่อนไปยังช่วงเวลาในวิดีโอ
      </div>
    </div>
  );
}