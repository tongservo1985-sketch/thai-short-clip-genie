"use client";

import React from 'react';
import { useEditorStore } from '@/store/useEditorStore';
import { Zap, TrendingUp, Star } from 'lucide-react';
import { motion } from 'framer-motion';

const MOCK_CLIPS = [
  { id: '1', title: 'The Hook: Intro', score: 98, start: 0, end: 15, tags: ['Hook', 'High Energy'] },
  { id: '2', title: 'Key Secret Revealed', score: 92, start: 45, end: 60, tags: ['Insight', 'Viral'] },
  { id: '3', title: 'Summary & CTA', score: 85, start: 120, end: 140, tags: ['CTA'] },
];

export default function ClipSidebar() {
  const { setActiveClip, activeClip } = useEditorStore();

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-slate-800 bg-brand-primary/5">
        <div className="flex items-center gap-2 text-brand-secondary mb-1">
          <Zap size={18} fill="currentColor" />
          <span className="font-bold text-sm">AI Viral Suggestions</span>
        </div>
        <p className="text-[11px] text-slate-400">เราเลือก 3 ช่วงที่ดีที่สุดสำหรับ TikTok/Reels</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {MOCK_CLIPS.map((clip) => (
          <motion.div
            key={clip.id}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setActiveClip({ 
              id: clip.id, 
              title: clip.title, 
              startTime: clip.start, 
              endTime: clip.end, 
              viralityScore: clip.score,
              reasoning: "AI detected high energy and clear Thai speech segmentation."
            })}
            className={clsx(
              "p-4 rounded-xl border cursor-pointer transition-all",
              activeClip?.id === clip.id 
                ? "bg-brand-primary/10 border-brand-primary shadow-lg shadow-brand-primary/5" 
                : "bg-slate-800/40 border-slate-700 hover:border-slate-500"
            )}
          >
            <div className="flex justify-between items-start mb-3">
              <h3 className="text-sm font-medium text-slate-200 leading-tight">
                {clip.title}
              </h3>
              <div className="flex items-center gap-1 bg-green-500/20 text-green-400 px-2 py-0.5 rounded text-[10px] font-bold">
                <TrendingUp size={10} />
                {clip.score}%
              </div>
            </div>

            <div className="flex gap-2">
              {clip.tags.map(tag => (
                <span key={tag} className="text-[9px] bg-slate-700 text-slate-300 px-1.5 py-0.5 rounded">
                  #{tag}
                </span>
              ))}
            </div>

            <div className="mt-4 flex items-center justify-between text-[10px] text-slate-500 font-mono">
              <span>00:{clip.start.toString().padStart(2, '0')}</span>
              <div className="h-[1px] flex-1 mx-2 bg-slate-700" />
              <span>00:{clip.end.toString().padStart(2, '0')}</span>
            </div>
          </motion.div>
        ))}
      </div>
      
      <button className="m-4 py-3 bg-gradient-to-r from-brand-primary to-brand-secondary rounded-lg font-bold text-sm shadow-xl shadow-brand-primary/20 hover:opacity-90 transition">
        Export All Viral Clips
      </button>
    </div>
  );
}