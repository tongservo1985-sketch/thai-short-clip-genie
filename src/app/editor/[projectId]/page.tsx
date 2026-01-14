"use client";

import React, { useEffect } from 'react';
import VideoPreview from '@/components/editor/VideoPreview';
import TranscriptView from '@/components/editor/TranscriptView';
import ClipSidebar from '@/components/editor/ClipSidebar';
import EditorNavbar from '@/components/editor/EditorNavbar';
import { useEditorStore } from '@/store/useEditorStore';

export default function CreatorStudio({ params }: { params: { projectId: string } }) {
  const { setTranscript } = useEditorStore();

  // Mock initial data load
  useEffect(() => {
    // In production, fetch from FastAPI /projects/{id}
    const mockTranscript = [
      { text: "สวัสดีครับ", start: 0.5, end: 1.2, confidence: 0.99 },
      { text: "วันนี้", start: 1.2, end: 1.5, confidence: 0.98 },
      { text: "เราจะมา", start: 1.5, end: 1.8, confidence: 0.95 },
      { text: "พูดถึง", start: 1.8, end: 2.1, confidence: 0.99 },
      { text: "เทคนิค", start: 2.1, end: 2.5, confidence: 0.97 },
      { text: "การสร้าง", start: 2.5, end: 3.0, confidence: 0.99 },
      { text: "รายได้", start: 3.0, end: 3.4, confidence: 0.98 },
      { text: "จากคลิปสั้น", start: 3.4, end: 4.2, confidence: 0.96 },
    ];
    setTranscript(mockTranscript);
  }, []);

  return (
    <div className="flex flex-col h-screen bg-brand-dark text-white overflow-hidden">
      <EditorNavbar projectId={params.projectId} />
      
      <main className="flex flex-1 overflow-hidden">
        {/* Left: AI Clip Recommendations */}
        <div className="w-80 border-r border-slate-800 bg-slate-900/50">
          <ClipSidebar />
        </div>

        {/* Center: Video Preview & Primary Controls */}
        <div className="flex-1 flex flex-col items-center justify-center p-8 bg-black/20">
          <VideoPreview />
        </div>

        {/* Right: Interactive Transcript Editor */}
        <div className="w-96 border-l border-slate-800 bg-slate-900/50">
          <TranscriptView />
        </div>
      </main>
    </div>
  );
}