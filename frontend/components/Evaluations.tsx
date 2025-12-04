import React from 'react';
import { Evaluation } from '../types';
import { Star, ThumbsUp, ThumbsDown, User, Bot } from 'lucide-react';

interface EvaluationsProps {
  evaluations: Evaluation[];
}

const Evaluations: React.FC<EvaluationsProps> = ({ evaluations }) => {
  return (
    <div className="h-full flex flex-col animate-fade-in">
      <header className="mb-6">
          <h1 className="text-2xl font-bold text-slate-900">AI Evaluations</h1>
          <p className="text-slate-500 text-sm">Review agent performance and fine-tune behavior.</p>
      </header>

      <div className="flex-1 grid grid-cols-12 gap-6 min-h-0">
        
        {/* List Pane */}
        <div className="col-span-4 bg-white border border-slate-200 rounded-xl overflow-hidden flex flex-col h-full">
            <div className="p-4 border-b border-slate-100 bg-slate-50">
                <h3 className="font-semibold text-slate-700 text-sm">Recent Conversations</h3>
            </div>
            <div className="overflow-y-auto flex-1">
                {evaluations.map((evaluation) => (
                    <div key={evaluation.id} className="p-4 border-b border-slate-100 hover:bg-slate-50 cursor-pointer transition-colors">
                        <div className="flex justify-between items-start mb-1">
                            <span className="text-sm font-medium text-slate-900">{evaluation.date}</span>
                            <div className={`px-2 py-0.5 rounded text-xs font-bold ${evaluation.qualityScore > 85 ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}`}>
                                Score: {evaluation.qualityScore}
                            </div>
                        </div>
                        <div className="flex items-center gap-2 mb-2">
                             <div className="flex gap-0.5">
                                {[1,2,3,4,5].map((s) => (
                                    <Star key={s} size={12} className={s <= Math.round(evaluation.qualityScore / 20) ? "text-amber-400 fill-amber-400" : "text-slate-200"} />
                                ))}
                             </div>
                             <span className="text-xs text-slate-400">{evaluation.duration}</span>
                        </div>
                        <div className="flex gap-1 flex-wrap">
                            {evaluation.tags.map(tag => (
                                <span key={tag} className="text-[10px] uppercase px-1.5 py-0.5 border border-slate-200 rounded text-slate-500">{tag}</span>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>

        {/* Detailed Review Pane */}
        <div className="col-span-8 bg-white border border-slate-200 rounded-xl flex flex-col h-full overflow-hidden">
             <div className="p-4 border-b border-slate-200 flex justify-between items-center bg-slate-50">
                <div className="flex items-center gap-2">
                    <h3 className="font-bold text-slate-900">Evaluation Report</h3>
                    <span className="text-slate-400 text-sm font-mono">#EV-2023-99</span>
                </div>
                <button className="text-sm font-medium text-brand-600 hover:text-brand-700 border border-brand-200 bg-brand-50 px-3 py-1 rounded-md">
                    Add to Training Set
                </button>
            </div>

            <div className="flex-1 grid grid-cols-2 divide-x divide-slate-200 min-h-0">
                {/* Transcript */}
                <div className="p-6 overflow-y-auto">
                    <h4 className="text-xs font-bold uppercase text-slate-400 tracking-wider mb-4">Transcript Synced</h4>
                    <div className="space-y-4 text-sm">
                        <div className="flex gap-3">
                            <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center flex-shrink-0"><User size={16} className="text-slate-600"/></div>
                            <div className="bg-slate-50 p-3 rounded-lg rounded-tl-none border border-slate-100">
                                <p className="text-slate-700">I noticed a charge for $200 I didn't authorize. I want a refund now.</p>
                                <div className="mt-1 flex items-center gap-1 text-xs text-red-400"><span className="font-semibold">Negative Sentiment</span></div>
                            </div>
                        </div>

                        <div className="flex gap-3 flex-row-reverse">
                            <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center flex-shrink-0"><Bot size={16} className="text-white"/></div>
                            <div className="bg-indigo-50 p-3 rounded-lg rounded-tr-none border border-indigo-100">
                                <p className="text-indigo-900">I completely understand your concern. That sounds stressful. Let me pull up your account immediately to investigate.</p>
                                <div className="mt-1 flex items-center gap-1 text-xs text-indigo-400"><span className="font-semibold">Empathy Detected</span></div>
                            </div>
                        </div>
                        
                         <div className="flex gap-3">
                            <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center flex-shrink-0"><User size={16} className="text-slate-600"/></div>
                            <div className="bg-slate-50 p-3 rounded-lg rounded-tl-none border border-slate-100">
                                <p className="text-slate-700">Okay, thank you. The order number is #4922.</p>
                                <div className="mt-1 flex items-center gap-1 text-xs text-emerald-500"><span className="font-semibold">Neutral/Positive Shift</span></div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Auto Grader */}
                <div className="p-6 bg-slate-50/50 overflow-y-auto">
                    <h4 className="text-xs font-bold uppercase text-slate-400 tracking-wider mb-4">Auto-Rubric</h4>
                    
                    <div className="space-y-4">
                        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-center mb-2">
                                <span className="text-sm font-semibold text-slate-800">Empathy & Tone</span>
                                <ThumbsUp size={16} className="text-emerald-500" />
                            </div>
                            <p className="text-xs text-slate-500">Agent acknowledged distress immediately using phrases "understand your concern" and "sounds stressful".</p>
                            <div className="mt-2 w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                                <div className="bg-emerald-500 h-full w-[95%]"></div>
                            </div>
                        </div>

                        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-center mb-2">
                                <span className="text-sm font-semibold text-slate-800">Policy Adherence</span>
                                <ThumbsUp size={16} className="text-emerald-500" />
                            </div>
                            <p className="text-xs text-slate-500">Agent verified identity before discussing transaction details. Correctly cited refund window.</p>
                             <div className="mt-2 w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                                <div className="bg-emerald-500 h-full w-[100%]"></div>
                            </div>
                        </div>

                        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-center mb-2">
                                <span className="text-sm font-semibold text-slate-800">Resolution Speed</span>
                                <ThumbsDown size={16} className="text-amber-500" />
                            </div>
                            <p className="text-xs text-slate-500">Verification step took longer than average (45s). Consider streamlining.</p>
                             <div className="mt-2 w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                                <div className="bg-amber-500 h-full w-[60%]"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default Evaluations;