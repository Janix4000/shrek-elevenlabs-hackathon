import React, { useState } from 'react';
import { Dispute, DisputeStatus, PaymentSource } from '../types';
import { XCircle, Database, ArrowRight, FileText, Sparkles, Upload, X, Search } from 'lucide-react';
import { analyzeDisputeTranscript } from '../services/geminiService';

interface DisputesProps {
  disputes: Dispute[];
}

const PaymentLogo: React.FC<{ source: PaymentSource }> = ({ source }) => {
  const logos: Record<PaymentSource, React.ReactElement> = {
    visa: (
      <img src="/Visa_Brandmark_Blue_RGB-1.png" alt="Visa" className="h-5 w-auto object-contain" />
    ),
    mastercard: (
      <svg viewBox="0 0 152 108" className="h-6 w-auto">
        <g fill="none" fillRule="evenodd">
          <rect width="152" height="108" fill="#000" rx="8"/>
          <circle cx="57" cy="54" r="31" fill="#EB001B"/>
          <circle cx="95" cy="54" r="31" fill="#F79E1B"/>
          <path fill="#FF5F00" d="M76 32.8c-5.9 4.6-9.7 11.7-9.7 19.7s3.8 15.1 9.7 19.7c5.9-4.6 9.7-11.7 9.7-19.7s-3.8-15.1-9.7-19.7z"/>
        </g>
      </svg>
    ),
    amex: (
      <img src="/amex.png" alt="American Express" className="h-5 w-auto object-contain" />
    ),
    paypal: (
      <svg viewBox="0 0 100 32" className="h-5 w-auto">
        <rect width="100" height="32" fill="#FFC439" rx="4"/>
        <g transform="translate(8, 8)">
          <path fill="#003087" d="M12.2 2.5c1.5 0 2.6.3 3.4 1 .7.7 1 1.8.7 3.2-.6 3.2-2.6 4.8-5.8 4.8h-1.4c-.2 0-.4.2-.5.4l-.5 3.2-.1.7c0 .2-.1.2-.3.2H5.3c-.2 0-.3-.1-.2-.3l2-12.8c0-.2.2-.4.4-.4h4.7z"/>
          <path fill="#009CDE" d="M8.5 6.5c0-.2.2-.4.4-.4h2.3c1.2 0 2.1.2 2.7.8.5.5.7 1.2.5 2.2-.4 2.2-1.7 3.3-3.9 3.3H9.2c-.2 0-.4.2-.4.4l-.4 2.7-.1.5c0 .1-.1.2-.2.2H6.8c-.1 0-.2-.1-.2-.2l1.3-8.5c0-.2.2-.4.4-.4l.2-1z"/>
        </g>
        <text x="38" y="21" fontFamily="Verdana, sans-serif" fontSize="10" fontWeight="bold" fill="#003087">PayPal</text>
      </svg>
    ),
    stripe: (
      <svg viewBox="0 0 60 25" className="h-6 w-auto">
        <g fill="#635BFF" fillRule="evenodd">
          <path d="M59.64 14.28h-8.06c.19 1.93 1.6 2.55 3.2 2.55 1.64 0 2.96-.37 4.05-.95v3.32a8.33 8.33 0 0 1-4.56 1.1c-4.01 0-6.83-2.5-6.83-7.48 0-4.19 2.39-7.52 6.3-7.52 3.92 0 5.96 3.28 5.96 7.5 0 .4-.04 1.26-.06 1.48zm-5.92-5.62c-1.03 0-2.17.73-2.17 2.58h4.25c0-1.85-1.07-2.58-2.08-2.58zM40.95 20.3c-1.44 0-2.32-.6-2.9-1.04l-.02 4.63-4.12.87V5.57h3.76l.08 1.02a4.7 4.7 0 0 1 3.23-1.29c2.9 0 5.62 2.6 5.62 7.4 0 5.23-2.7 7.6-5.65 7.6zM40 8.95c-.95 0-1.54.34-1.97.81l.02 6.12c.4.44.98.78 1.95.78 1.52 0 2.54-1.65 2.54-3.87 0-2.15-1.04-3.84-2.54-3.84zM28.24 5.57h4.13v14.44h-4.13V5.57zm0-4.7L32.37 0v3.36l-4.13.88V.88zm-4.32 9.35v9.79H19.8V5.57h3.7l.12 1.22c1-1.77 3.07-1.41 3.62-1.22v3.79c-.52-.17-2.29-.43-3.32.86zm-8.55 4.72c0 2.43 2.6 1.68 3.12 1.46v3.36c-.55.3-1.54.54-2.89.54a4.15 4.15 0 0 1-4.27-4.24l.01-13.17 4.02-.86v3.54h3.14V9.1h-3.13v5.85zm-4.91.7c0 2.97-2.31 4.66-5.73 4.66a11.2 11.2 0 0 1-4.46-.93v-3.93c1.38.75 3.1 1.31 4.46 1.31.92 0 1.53-.24 1.53-1C6.26 13.77 0 14.51 0 9.95 0 7.04 2.28 5.3 5.62 5.3c1.36 0 2.72.2 4.09.75v3.88a9.23 9.23 0 0 0-4.1-1.06c-.86 0-1.44.25-1.44.93 0 1.85 6.29.97 6.29 5.88z"/>
        </g>
      </svg>
    ),
    klarna: (
      <svg viewBox="0 0 80 32" className="h-6 w-auto">
        <rect width="80" height="32" fill="#FFB3C7" rx="4"/>
        <text x="40" y="21" fontFamily="Arial, sans-serif" fontSize="14" fontWeight="bold" fill="#000000" textAnchor="middle">klarna</text>
      </svg>
    ),
  };

  return <div className="flex items-center justify-center shrink-0">{logos[source]}</div>;
};

const Disputes: React.FC<DisputesProps> = ({ disputes }) => {
  const [selectedDispute, setSelectedDispute] = useState<Dispute | null>(null);
  const [analysis, setAnalysis] = useState<{recommendation: string, reasoning: string, confidence: number} | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [activeTab, setActiveTab] = useState('All Disputes');
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSelect = (dispute: Dispute) => {
    setSelectedDispute(dispute);
    setAnalysis(null);
    setUploadedFiles([]);
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      const pdfFiles = Array.from(files).filter(file => file.type === 'application/pdf');
      setUploadedFiles(prev => [...prev, ...pdfFiles]);
    }
  };

  const removeFile = (index: number) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const runAnalysis = async () => {
    if (!selectedDispute) return;
    setIsAnalyzing(true);
    const result = await analyzeDisputeTranscript(selectedDispute.transcript, selectedDispute.amount, selectedDispute.customerName);
    setAnalysis(result);
    setIsAnalyzing(false);
  };

  const tabs = ['All Disputes', 'Action Required', 'Won', 'Lost'];

  // Filter disputes based on active tab and search query
  let filteredDisputes = activeTab === 'All Disputes'
    ? disputes
    : activeTab === 'Action Required'
    ? disputes.filter(d => d.status === DisputeStatus.ActionRequired)
    : activeTab === 'Won'
    ? disputes.filter(d => d.status === DisputeStatus.Won)
    : activeTab === 'Lost'
    ? disputes.filter(d => d.status === DisputeStatus.Lost)
    : disputes;

  // Apply search filter
  if (searchQuery) {
    filteredDisputes = filteredDisputes.filter(d =>
      d.customerName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      d.orderItems.some(item => item.toLowerCase().includes(searchQuery.toLowerCase())) ||
      d.amount.toString().includes(searchQuery)
    );
  }

  return (
    <div className="animate-fade-in space-y-8">

      {/* Simple Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Dispute Resolution</h1>
      </div>

      {/* Tab Navigation and Search */}
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          {tabs.map(tab => (
              <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 ${
                      activeTab === tab
                      ? 'bg-gradient-to-r from-slate-900 to-slate-700 text-white shadow-lg shadow-slate-900/25 scale-105'
                      : 'bg-white border border-slate-200 text-slate-600 hover:border-slate-300 hover:shadow-md hover:scale-102'
                  }`}
              >
                  {tab}
              </button>
          ))}
        </div>

        {/* Search Box */}
        <div className="relative w-80">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
          <input
            type="text"
            placeholder="Search by customer, product, or amount..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-transparent"
          />
        </div>
      </div>

      {/* Table Layout */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Payment</th>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Customer</th>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Product</th>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Amount</th>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">GuardScore</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {filteredDisputes.map((dispute) => (
              <tr
                key={dispute.id}
                onClick={() => handleSelect(dispute)}
                className="hover:bg-slate-50 cursor-pointer transition-colors"
              >
                <td className="px-6 py-5">
                  <div className="w-12 h-12 bg-slate-50 rounded-lg flex items-center justify-center">
                    <PaymentLogo source={dispute.paymentSource} />
                  </div>
                </td>
                <td className="px-6 py-5">
                  <div className="text-base font-bold text-slate-900">{dispute.customerName}</div>
                  <div className="text-xs text-slate-500 mt-0.5">{dispute.date}</div>
                </td>
                <td className="px-6 py-5">
                  <div className="text-sm text-slate-600">{dispute.orderItems.join(', ')}</div>
                </td>
                <td className="px-6 py-5">
                  <span className={`px-3 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider inline-block ${
                      dispute.status === DisputeStatus.ActionRequired
                      ? 'bg-amber-100 text-amber-700'
                      : dispute.status === DisputeStatus.Won
                      ? 'bg-emerald-100 text-emerald-700'
                      : dispute.status === DisputeStatus.Lost
                      ? 'bg-red-100 text-red-700'
                      : 'bg-indigo-100 text-indigo-700'
                  }`}>
                    {dispute.status}
                  </span>
                </td>
                <td className="px-6 py-5 text-right">
                  <div className="text-lg font-bold text-slate-900">${dispute.amount.toFixed(2)}</div>
                </td>
                <td className="px-6 py-5 text-right">
                  <div className={`text-lg font-bold ${dispute.confidenceScore > 50 ? 'text-emerald-600' : 'text-amber-600'}`}>
                    {dispute.confidenceScore}%
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

       {/* Enhanced Drawer Overlay */}
      {selectedDispute && (
        <>
          <div
            className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm z-40 transition-opacity animate-fade-in"
            onClick={() => setSelectedDispute(null)}
          ></div>
          <div className="fixed inset-y-0 right-0 w-[520px] bg-gradient-to-br from-white via-white to-slate-50/30 shadow-2xl z-50 transform transition-transform border-l border-slate-200/80 flex flex-col animate-slide-in-right">

            <div className="p-6 border-b border-slate-200/80 flex justify-between items-center bg-gradient-to-r from-white to-slate-50/50">
                <div>
                    <h2 className="text-xl font-black text-slate-900 tracking-tight">Dispute Review</h2>
                    <p className="text-xs text-slate-500 font-mono mt-1 bg-slate-100 px-2 py-0.5 rounded inline-block">ID: {selectedDispute.id}</p>
                </div>
                <div className="flex gap-2">
                     <button onClick={() => setSelectedDispute(null)} className="p-2.5 hover:bg-slate-100 rounded-xl text-slate-400 hover:text-slate-600 transition-all hover:scale-110">
                        <XCircle size={22} />
                     </button>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-7">

                 {/* Modern Transcript Card */}
                 <div className="space-y-3">
                    <h3 className="text-xs font-black uppercase text-slate-500 tracking-widest flex items-center gap-2">
                      <div className="w-1 h-4 bg-gradient-to-b from-indigo-500 to-purple-500 rounded-full"></div>
                      Voice Agent Transcript
                    </h3>
                    <div className="bg-gradient-to-br from-slate-50 to-slate-100/50 rounded-2xl p-5 border border-slate-200 shadow-sm text-sm leading-relaxed space-y-3">
                        {selectedDispute.transcript.split('\n').map((line, i) => (
                             <p key={i} className={line.startsWith('Agent:') ? 'text-indigo-700 font-bold bg-indigo-50 px-3 py-2 rounded-lg border border-indigo-100' : 'text-slate-700 font-medium px-3 py-2'}>
                                {line}
                             </p>
                        ))}
                    </div>
                 </div>

                 {/* Enhanced RAG Pipeline with Modern Gradients */}
                 {isAnalyzing && (
                   <div className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 border-2 border-indigo-200 rounded-2xl p-6 shadow-lg">
                     <h3 className="text-sm font-black uppercase text-indigo-900 tracking-widest mb-5 flex items-center gap-2">
                       <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center shadow-md">
                         <Database size={16} className="text-white" />
                       </div>
                       RAG Pipeline Processing
                     </h3>

                     <div className="space-y-4">
                       {/* Step 1: Query */}
                       <div className="flex items-start gap-4 animate-fade-in bg-white/60 backdrop-blur-sm rounded-xl p-4 border border-blue-100 shadow-sm">
                         <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-blue-500 flex items-center justify-center text-white text-sm font-black flex-shrink-0 shadow-lg shadow-blue-500/30">1</div>
                         <div className="flex-1">
                           <div className="font-bold text-base text-slate-900 mb-1.5">Query Embedding</div>
                           <div className="text-xs text-slate-600 font-medium mb-3">Converting transcript to vector representation...</div>
                           <div className="h-2 bg-blue-100 rounded-full overflow-hidden shadow-inner">
                             <div className="h-full bg-gradient-to-r from-blue-600 to-blue-500 animate-pulse shadow-sm" style={{width: '100%'}}></div>
                           </div>
                         </div>
                       </div>

                       {/* Arrow */}
                       <div className="flex justify-center">
                         <ArrowRight size={18} className="text-indigo-300" strokeWidth={3} />
                       </div>

                       {/* Step 2: Retrieval */}
                       <div className="flex items-start gap-4 animate-fade-in bg-white/60 backdrop-blur-sm rounded-xl p-4 border border-purple-100 shadow-sm" style={{animationDelay: '0.2s'}}>
                         <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-600 to-purple-500 flex items-center justify-center text-white text-sm font-black flex-shrink-0 shadow-lg shadow-purple-500/30">2</div>
                         <div className="flex-1">
                           <div className="font-bold text-base text-slate-900 mb-1.5">Knowledge Retrieval</div>
                           <div className="text-xs text-slate-600 font-medium mb-3">Searching policy database for relevant context...</div>
                           <div className="flex flex-wrap gap-2">
                             <div className="px-3 py-1.5 bg-gradient-to-r from-purple-100 to-purple-50 text-purple-700 rounded-lg text-xs font-bold border border-purple-200 shadow-sm">Return Policy</div>
                             <div className="px-3 py-1.5 bg-gradient-to-r from-purple-100 to-purple-50 text-purple-700 rounded-lg text-xs font-bold border border-purple-200 shadow-sm">Fraud Guidelines</div>
                             <div className="px-3 py-1.5 bg-gradient-to-r from-purple-100 to-purple-50 text-purple-700 rounded-lg text-xs font-bold border border-purple-200 shadow-sm">Past Cases</div>
                           </div>
                         </div>
                       </div>

                       {/* Arrow */}
                       <div className="flex justify-center">
                         <ArrowRight size={18} className="text-indigo-300" strokeWidth={3} />
                       </div>

                       {/* Step 3: Augmentation */}
                       <div className="flex items-start gap-4 animate-fade-in bg-white/60 backdrop-blur-sm rounded-xl p-4 border border-indigo-100 shadow-sm" style={{animationDelay: '0.4s'}}>
                         <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-600 to-indigo-500 flex items-center justify-center text-white text-sm font-black flex-shrink-0 shadow-lg shadow-indigo-500/30">3</div>
                         <div className="flex-1">
                           <div className="font-bold text-base text-slate-900 mb-1.5">Context Augmentation</div>
                           <div className="text-xs text-slate-600 font-medium mb-3">Enriching prompt with retrieved knowledge...</div>
                           <div className="bg-gradient-to-r from-indigo-100 to-indigo-50 rounded-lg p-3 text-xs text-indigo-900 font-bold border border-indigo-200 shadow-sm flex items-center gap-2">
                             <FileText size={14} className="text-indigo-600" />
                             3 documents • 2,847 tokens
                           </div>
                         </div>
                       </div>

                       {/* Arrow */}
                       <div className="flex justify-center">
                         <ArrowRight size={18} className="text-indigo-300" strokeWidth={3} />
                       </div>

                       {/* Step 4: Generation */}
                       <div className="flex items-start gap-4 animate-fade-in bg-white/60 backdrop-blur-sm rounded-xl p-4 border border-pink-100 shadow-sm" style={{animationDelay: '0.6s'}}>
                         <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-pink-600 to-pink-500 flex items-center justify-center text-white text-sm font-black flex-shrink-0 shadow-lg shadow-pink-500/30">4</div>
                         <div className="flex-1">
                           <div className="font-bold text-base text-slate-900 mb-1.5 flex items-center gap-2">
                             <Sparkles size={16} className="text-pink-600" />
                             AI Generation
                           </div>
                           <div className="text-xs text-slate-600 font-medium mb-3">Generating recommendation with context...</div>
                           <div className="flex items-center gap-3">
                             <div className="flex-1 h-2 bg-pink-100 rounded-full overflow-hidden shadow-inner">
                               <div className="h-full bg-gradient-to-r from-pink-600 to-pink-500 animate-pulse shadow-sm" style={{width: '75%'}}></div>
                             </div>
                             <span className="text-sm text-pink-600 font-black">75%</span>
                           </div>
                         </div>
                       </div>
                     </div>
                   </div>
                 )}

                 {/* Enhanced AI Recommendation Card */}
                <div className="bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 border-2 border-indigo-200 rounded-2xl p-6 shadow-lg">
                     <div className="flex justify-between items-center mb-5">
                        <h3 className="text-sm font-black uppercase text-indigo-900 tracking-widest flex items-center gap-2">
                          <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center shadow-md">
                            <Sparkles size={16} className="text-white" />
                          </div>
                          AI Recommendation
                        </h3>
                        {!analysis && (
                            <button onClick={runAnalysis} className="text-xs bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-4 py-2 rounded-xl font-bold hover:from-indigo-700 hover:to-purple-700 shadow-lg shadow-indigo-500/30 transition-all hover:scale-105">
                                {isAnalyzing ? 'Analyzing...' : 'Analyze'}
                            </button>
                        )}
                     </div>

                     {analysis && (
                        <div className="space-y-4 animate-fade-in">
                             <div className="flex items-center gap-3 bg-white/70 backdrop-blur-sm rounded-xl p-4 border border-indigo-100 shadow-sm">
                                <span className="text-3xl font-black bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">{analysis.recommendation}</span>
                             </div>
                             <p className="text-sm text-slate-700 font-medium leading-relaxed bg-white/50 rounded-lg p-4 border border-indigo-100">{analysis.reasoning}</p>
                             <div className="bg-white/70 rounded-xl p-4 border border-indigo-100">
                               <div className="h-2 bg-indigo-100 rounded-full w-full overflow-hidden shadow-inner">
                                   <div className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 shadow-sm" style={{width: `${analysis.confidence}%`}}></div>
                               </div>
                               <p className="text-xs text-indigo-600 font-black text-right mt-2">{analysis.confidence}% Confidence</p>
                             </div>
                        </div>
                     )}
                </div>

            </div>

            <div className="p-6 border-t-2 border-slate-200 space-y-4 bg-gradient-to-br from-white to-slate-50/50">
                 {/* Modern Upload Section */}
                 <div className="space-y-3">
                   <label className="block text-xs font-black text-slate-700 uppercase tracking-widest flex items-center gap-2">
                     <div className="w-1 h-4 bg-gradient-to-b from-blue-500 to-indigo-500 rounded-full"></div>
                     Evidence Documents
                   </label>

                   {/* Uploaded Files List */}
                   {uploadedFiles.length > 0 && (
                     <div className="space-y-2 mb-2">
                       {uploadedFiles.map((file, index) => (
                         <div key={index} className="flex items-center justify-between bg-gradient-to-r from-slate-50 to-slate-100/50 border border-slate-200 rounded-xl px-4 py-3 shadow-sm group hover:shadow-md transition-all">
                           <div className="flex items-center gap-3 flex-1 min-w-0">
                             <div className="w-8 h-8 bg-gradient-to-br from-red-50 to-red-100 rounded-lg flex items-center justify-center border border-red-200">
                               <FileText size={16} className="text-red-600" />
                             </div>
                             <div className="flex-1 min-w-0">
                               <span className="text-sm text-slate-900 font-bold truncate block">{file.name}</span>
                               <span className="text-xs text-slate-400 font-medium">
                                 {(file.size / 1024).toFixed(1)} KB
                               </span>
                             </div>
                           </div>
                           <button
                             onClick={() => removeFile(index)}
                             className="p-2 hover:bg-red-100 rounded-lg transition-all flex-shrink-0 group-hover:scale-110"
                           >
                             <X size={16} className="text-slate-400 hover:text-red-600" />
                           </button>
                         </div>
                       ))}
                     </div>
                   )}

                   {/* Modern Upload Button */}
                   <label className="flex items-center justify-center gap-3 px-5 py-4 border-2 border-dashed border-slate-300 text-slate-600 font-bold text-sm rounded-xl hover:bg-slate-50 hover:border-indigo-400 cursor-pointer transition-all hover:shadow-md group">
                     <div className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center group-hover:bg-indigo-100 transition-colors">
                       <Upload size={18} className="text-slate-600 group-hover:text-indigo-600" />
                     </div>
                     <span className="group-hover:text-indigo-600 transition-colors">Upload PDF Evidence</span>
                     <input
                       type="file"
                       accept=".pdf,application/pdf"
                       multiple
                       onChange={handleFileUpload}
                       className="hidden"
                     />
                   </label>
                   <p className="text-xs text-slate-400 font-medium">Accepted formats: PDF only</p>
                 </div>

                 {/* Enhanced Action Buttons */}
                 <div className="flex gap-3 pt-2">
                   <button className="flex-1 py-3 border-2 border-slate-200 text-slate-700 font-bold text-sm rounded-xl hover:bg-slate-50 hover:border-slate-300 transition-all hover:shadow-md">
                      Ignore
                   </button>
                   <button
                     className={`flex-1 py-3 font-bold text-sm rounded-xl transition-all ${
                       uploadedFiles.length > 0
                         ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:scale-105'
                         : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                     }`}
                     disabled={uploadedFiles.length === 0}
                   >
                      Submit Evidence ({uploadedFiles.length})
                   </button>
                 </div>
            </div>
          </div>
        </>
      )}

    </div>
  );
};

export default Disputes;
