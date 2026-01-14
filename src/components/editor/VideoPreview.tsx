"use client";

import React, { useRef, useEffect } from 'react';
import { Play, Pause, RotateCcw, Maximize, Smartphone, Monitor } from 'lucide-react';
import { useEditorStore } from '@/store/useEditorStore';
import * as Slider from '@radix-ui/react-slider';

export default function VideoPreview() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const { isPlaying, setIsPlaying, currentTime, setCurrentTime } = useEditorStore();
  const [aspectRatio, setAspectRatio] = React.useState<'9:16' | '16:9'>('9:16');

  useEffect(() => {
    if (videoRef.current) {
      if (Math.abs(videoRef.current.currentTime - currentTime) > 0.5) {
        videoRef.current.currentTime = currentTime;
      }
    }
  }, [currentTime]);

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) videoRef.current.pause();
      else videoRef.current.play();
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <div className="w-full h-full flex flex-col items-center">
      {/* Aspect Ratio Toggles */}
      <div className="flex bg-slate-800 p-1 rounded-full mb-6">
        <button 
          onClick={() => setAspectRatio('9:16')}
          className={clsx("flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-medium transition", 
          aspectRatio === '9:16' ? "bg-brand-primary text-white" : "text-slate-400")}
        >
          <Smartphone size={14} /> Vertical
        </button>
        <button 
          onClick={() => setAspectRatio('16:9')}
          className={clsx("flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-medium transition", 
          aspectRatio === '16:9' ? "bg-brand-primary text-white" : "text-slate-400")}
        >
          <Monitor size={14} /> Original
        </button>
      </div>

      {/* Video Container */}
      <div className={clsx(
        "relative bg-black shadow-2xl transition-all duration-500 overflow-hidden rounded-xl border border-white/10",
        aspectRatio === '9:16' ? "aspect-[9/16] h-[550px]" : "aspect-video w-[800px]"
      )}>
        <video 
          ref={videoRef}
          className="w-full h-full object-cover"
          onTimeUpdate={(e) => setCurrentTime(e.currentTarget.currentTime)}
          src="https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4"
        />
        
        {/* Playback Overlay */}
        <div className="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity bg-black/20">
           <button onClick={togglePlay} className="p-4 bg-white/20 backdrop-blur-md rounded-full border border-white/30">
              {isPlaying ? <Pause fill="white" /> : <Play fill="white" />}
           </button>
        </div>
      </div>

      {/* Custom Timeline Tool */}
      <div className="w-full max-w-2xl mt-8 space-y-4">
        <Slider.Root 
          className="relative flex items-center select-none touch-none w-full h-5"
          value={[currentTime]}
          max={60} // Mock duration
          step={0.1}
          onValueChange={([val]) => setCurrentTime(val)}
        >
          <Slider.Track className="bg-slate-700 relative grow h-[4px] rounded-full">
            <Slider.Range className="absolute bg-brand-primary h-full rounded-full" />
          </Slider.Track>
          <Slider.Thumb className="block w-4 h-4 bg-white shadow-xl rounded-full focus:outline-none ring-2 ring-brand-primary" />
        </Slider.Root>
        
        <div className="flex justify-between text-xs text-slate-500 font-mono">
          <span>{currentTime.toFixed(2)}s</span>
          <div className="flex gap-6">
            <RotateCcw size={16} className="cursor-pointer hover:text-white" />
            <Maximize size={16} className="cursor-pointer hover:text-white" />
          </div>
          <span>01:00.00</span>
        </div>
      </div>
    </div>
  );
}