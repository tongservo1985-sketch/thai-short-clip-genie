import { create } from 'zustand';

interface Word {
  text: string;
  start: number;
  end: number;
  confidence: number;
}

interface Clip {
  id: string;
  title: string;
  startTime: number;
  endTime: number;
  viralityScore: number;
  reasoning: string;
}

interface EditorState {
  currentTime: number;
  isPlaying: boolean;
  activeClip: Clip | null;
  transcript: Word[];
  setCurrentTime: (time: number) => void;
  setIsPlaying: (playing: boolean) => void;
  setActiveClip: (clip: Clip) => void;
  setTranscript: (words: Word[]) => void;
}

export const useEditorStore = create<EditorState>((set) => ({
  currentTime: 0,
  isPlaying: false,
  activeClip: null,
  transcript: [],
  setCurrentTime: (time) => set({ currentTime: time }),
  setIsPlaying: (playing) => set({ isPlaying: playing }),
  setActiveClip: (clip) => set({ activeClip: clip, currentTime: clip.startTime }),
  setTranscript: (words) => set({ transcript: words }),
}));