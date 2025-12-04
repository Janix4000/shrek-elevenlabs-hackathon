import React, { useState } from 'react';
import { KPIMetrics } from '../types';
import { Clock, TrendingUp, AlertCircle, DollarSign, MoreHorizontal, Globe, ZoomIn, ZoomOut } from 'lucide-react';
import { ComposableMap, Geographies, Geography, ZoomableGroup } from 'react-simple-maps';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface DashboardProps {
  metrics: KPIMetrics;
}

const DonutChart = () => {
    const circumference = 251;
    // Percentages: 39.04%, 18.78%, 12.56%, 9.85% (remaining 19.77% grouped as "Other")
    const segments = [
        { color: '#3b82f6', percent: 39.04, offset: 0 },           // Blue - Fraud
        { color: '#0ea5e9', percent: 18.78, offset: 39.04 },       // Sky - Canceled Recurring
        { color: '#1e293b', percent: 12.56, offset: 57.82 },       // Slate - Not As Described
        { color: '#a855f7', percent: 9.85, offset: 70.38 },        // Purple - Product Not Received
        { color: '#94a3b8', percent: 19.77, offset: 80.23 },       // Gray - Other (combined remaining)
    ];

    return (
        <div className="relative w-52 h-52">
            <svg viewBox="0 0 100 100" className="transform -rotate-90 w-full h-full">
                <circle cx="50" cy="50" r="40" stroke="#f1f5f9" strokeWidth="20" fill="none" />
                {segments.map((segment, i) => (
                    <circle
                        key={i}
                        cx="50"
                        cy="50"
                        r="40"
                        stroke={segment.color}
                        strokeWidth="20"
                        fill="none"
                        strokeDasharray={`${(segment.percent / 100) * circumference} ${circumference}`}
                        strokeDashoffset={-(segment.offset / 100) * circumference}
                    />
                ))}
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
                 <span className="text-xl font-extrabold text-slate-900">$418.3k</span>
                 <span className="text-xs text-slate-400 font-medium">Total Value</span>
            </div>
        </div>
    );
};

const Dashboard: React.FC<DashboardProps> = ({ metrics }) => {
  const [mapZoom, setMapZoom] = useState(1);
  const [mapCenter, setMapCenter] = useState<[number, number]>([10, 20]);

  const handleZoomIn = () => setMapZoom(prev => Math.min(prev + 0.5, 4));
  const handleZoomOut = () => setMapZoom(prev => Math.max(prev - 0.5, 1));
  const handleResetZoom = () => {
    setMapZoom(1);
    setMapCenter([10, 20]);
  };

  return (
    <div className="h-full flex flex-col gap-6 animate-fade-in pb-12">

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="text-slate-500 text-sm mt-1">Overview of dispute resolution performance and metrics</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 flex-shrink-0">
        <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
          <div className="flex items-center gap-2 text-slate-500 text-xs uppercase tracking-wider font-bold mb-3">
            <DollarSign size={16} />
            <span>Total Value</span>
          </div>
          <div className="text-3xl font-bold text-slate-900 mb-2">$4.2M</div>
          <div className="text-xs text-emerald-600 font-semibold">↗ 12.3% vs last period</div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
          <div className="flex items-center gap-2 text-slate-500 text-xs uppercase tracking-wider font-bold mb-3">
            <TrendingUp size={16} />
            <span>Win Rate</span>
          </div>
          <div className="text-3xl font-bold text-slate-900 mb-2">82%</div>
          <div className="text-xs text-emerald-600 font-semibold">↗ 4.2% vs last period</div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
          <div className="flex items-center gap-2 text-slate-500 text-xs uppercase tracking-wider font-bold mb-3">
            <Clock size={16} />
            <span>Time Saved</span>
          </div>
          <div className="text-3xl font-bold text-slate-900 mb-2">3,452h</div>
          <div className="text-xs text-emerald-600 font-semibold">↗ 8.7% vs last period</div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
          <div className="flex items-center gap-2 text-slate-500 text-xs uppercase tracking-wider font-bold mb-3">
            <AlertCircle size={16} />
            <span>Fraud Rate</span>
          </div>
          <div className="text-3xl font-bold text-slate-900 mb-2">6.5%</div>
          <div className="text-xs text-emerald-600 font-semibold">↗ 2.1% vs last period</div>
        </div>
      </div>

      {/* Two Column Layout: Disputes by Reason and Win Rate Trend */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 flex-shrink-0">

        {/* Disputes by Reason with Pie Chart */}
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
          <div className="mb-6">
            <h3 className="font-bold text-slate-900 text-lg">Disputes by Reason</h3>
            <p className="text-xs text-slate-500 mt-1">Last 12 Months</p>
          </div>

          <div className="flex items-center gap-8">
            {/* Table on the left */}
            <div className="flex-1">
              <table className="w-full text-left border-collapse">
                <thead className="bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="px-4 py-3 text-xs font-bold text-slate-500 uppercase tracking-wider">Reason</th>
                    <th className="px-4 py-3 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Amount</th>
                    <th className="px-4 py-3 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Percentage</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  <tr className="hover:bg-slate-50 transition-colors">
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                        <span className="text-sm font-bold text-slate-900">Fraud</span>
                      </div>
                    </td>
                    <td className="px-4 py-4 text-right">
                      <span className="text-base font-bold text-slate-900">$163.3k</span>
                    </td>
                    <td className="px-4 py-4 text-right">
                      <span className="text-base font-bold text-slate-900">39.04%</span>
                    </td>
                  </tr>
                  <tr className="hover:bg-slate-50 transition-colors">
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-3 h-3 bg-sky-500 rounded-full"></div>
                        <span className="text-sm font-bold text-slate-900">Canceled Recurring</span>
                      </div>
                    </td>
                    <td className="px-4 py-4 text-right">
                      <span className="text-base font-bold text-slate-900">$78.6k</span>
                    </td>
                    <td className="px-4 py-4 text-right">
                      <span className="text-base font-bold text-slate-900">18.78%</span>
                    </td>
                  </tr>
                  <tr className="hover:bg-slate-50 transition-colors">
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-3 h-3 bg-slate-800 rounded-full"></div>
                        <span className="text-sm font-bold text-slate-900">Not As Described</span>
                      </div>
                    </td>
                    <td className="px-4 py-4 text-right">
                      <span className="text-base font-bold text-slate-900">$52.5k</span>
                    </td>
                    <td className="px-4 py-4 text-right">
                      <span className="text-base font-bold text-slate-900">12.56%</span>
                    </td>
                  </tr>
                  <tr className="hover:bg-slate-50 transition-colors">
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                        <span className="text-sm font-bold text-slate-900">Product Not Received</span>
                      </div>
                    </td>
                    <td className="px-4 py-4 text-right">
                      <span className="text-base font-bold text-slate-900">$41.2k</span>
                    </td>
                    <td className="px-4 py-4 text-right">
                      <span className="text-base font-bold text-slate-900">9.85%</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Pie chart on the right */}
            <div className="flex-shrink-0 flex items-center justify-center">
              <DonutChart />
            </div>
          </div>
        </div>

        {/* Win Rate Trend Chart */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h3 className="font-bold text-slate-900 text-lg">Win Rate Trend</h3>
              <p className="text-xs text-slate-500 mt-1">Last 12 Months</p>
            </div>
            <button className="text-slate-400 hover:text-slate-600 transition-colors"><MoreHorizontal size={16} /></button>
          </div>

          {/* Bar Chart */}
          <div className="h-[200px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={[
                  { month: 'Jan', rate: 52 },
                  { month: 'Feb', rate: 56 },
                  { month: 'Mar', rate: 60 },
                  { month: 'Apr', rate: 64 },
                  { month: 'May', rate: 68 },
                  { month: 'Jun', rate: 71 },
                  { month: 'Jul', rate: 73 },
                  { month: 'Aug', rate: 76 },
                  { month: 'Sep', rate: 78 },
                  { month: 'Oct', rate: 80 },
                  { month: 'Nov', rate: 81 },
                  { month: 'Dec', rate: 82 },
                ]}
                margin={{ top: 20, right: 10, left: -20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                <XAxis
                  dataKey="month"
                  tick={{ fill: '#94a3b8', fontSize: 10 }}
                  axisLine={{ stroke: '#cbd5e1' }}
                  tickLine={false}
                />
                <YAxis
                  domain={[0, 100]}
                  tick={{ fill: '#94a3b8', fontSize: 10 }}
                  axisLine={{ stroke: '#cbd5e1' }}
                  tickLine={false}
                  tickFormatter={(value) => `${value}%`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: 'none',
                    borderRadius: '6px',
                    fontSize: '12px',
                    color: '#fff'
                  }}
                  formatter={(value: number) => [`${value}%`, 'Win Rate']}
                  cursor={{ fill: '#f1f5f9' }}
                />
                <Bar
                  dataKey="rate"
                  fill="url(#colorGradient)"
                  radius={[4, 4, 0, 0]}
                />
                <defs>
                  <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#10b981" stopOpacity={1}/>
                    <stop offset="100%" stopColor="#059669" stopOpacity={1}/>
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="mt-3 pt-3 border-t border-slate-200">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-xs text-slate-500">Current Rate</div>
                <div className="text-xl font-bold text-slate-900">82%</div>
              </div>
              <div className="text-right">
                <div className="text-xs text-slate-500">vs Last Month</div>
                <div className="text-base font-bold text-emerald-600">↗ 1.2%</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Geographical Win Rates Map */}
      <div style={{ minHeight: '800px' }}>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col" style={{ height: '800px' }}>
          <div className="flex justify-between items-center mb-6">
            <div>
              <h3 className="font-bold text-slate-900 text-lg flex items-center gap-2">
                <Globe size={18} className="text-blue-500" />
                Win Rates by Country
              </h3>
              <p className="text-xs text-slate-500 mt-1">Last 6 Months</p>
            </div>
            <button className="text-slate-400 hover:text-slate-600 transition-colors"><MoreHorizontal size={16} /></button>
          </div>

          <div className="relative flex-1 min-h-0">
            {/* Zoom Controls */}
            <div className="absolute top-2 right-2 z-10 flex flex-col gap-1 bg-white rounded-lg shadow-md border border-slate-200 p-1">
              <button
                onClick={handleZoomIn}
                disabled={mapZoom >= 4}
                className="p-1.5 hover:bg-slate-100 rounded disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                title="Zoom In"
              >
                <ZoomIn size={16} className="text-slate-700" />
              </button>
              <button
                onClick={handleResetZoom}
                className="px-1.5 py-1 text-[10px] font-medium text-slate-700 hover:bg-slate-100 rounded transition-colors"
                title="Reset Zoom"
              >
                {Math.round(mapZoom * 100)}%
              </button>
              <button
                onClick={handleZoomOut}
                disabled={mapZoom <= 1}
                className="p-1.5 hover:bg-slate-100 rounded disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                title="Zoom Out"
              >
                <ZoomOut size={16} className="text-slate-700" />
              </button>
            </div>

            <ComposableMap
              projection="geoMercator"
              projectionConfig={{
                scale: 100,
                center: [10, 20]
              }}
              width={800}
              height={400}
              style={{ width: '100%', height: '100%', maxHeight: '100%' }}
            >
              <ZoomableGroup zoom={mapZoom} center={mapCenter} onMoveEnd={(position) => setMapCenter(position.coordinates)}>
                <Geographies geography="https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json">
                  {({ geographies }) =>
                    geographies.map((geo) => {
                    // Map country codes to win rates and colors (using numeric IDs from world-atlas)
                    const countryData: Record<string, { rate: number; color: string }> = {
                      // North America - Lower win rates
                      '840': { rate: 42.5, color: '#3b82f6' },  // USA - Blue
                      '124': { rate: 44.8, color: '#3b82f6' },  // Canada - Blue
                      '484': { rate: 38.2, color: '#f97316' },  // Mexico - Orange

                      // Western Europe - Higher win rates
                      '826': { rate: 68.4, color: '#10b981' },  // United Kingdom - Green
                      '276': { rate: 72.1, color: '#10b981' },  // Germany - Green
                      '250': { rate: 71.3, color: '#10b981' },  // France - Green
                      '380': { rate: 66.8, color: '#10b981' },  // Italy - Green
                      '724': { rate: 69.2, color: '#10b981' },  // Spain - Green
                      '528': { rate: 74.9, color: '#10b981' },  // Netherlands - Green
                      '056': { rate: 73.5, color: '#10b981' },  // Belgium - Green
                      '040': { rate: 71.8, color: '#10b981' },  // Austria - Green
                      '756': { rate: 75.2, color: '#10b981' },  // Switzerland - Green
                      '752': { rate: 70.6, color: '#10b981' },  // Sweden - Green
                      '578': { rate: 72.8, color: '#10b981' },  // Norway - Green
                      '208': { rate: 73.1, color: '#10b981' },  // Denmark - Green
                      '246': { rate: 71.5, color: '#10b981' },  // Finland - Green
                      '372': { rate: 68.9, color: '#10b981' },  // Ireland - Green
                      '620': { rate: 70.2, color: '#10b981' },  // Portugal - Green
                      '300': { rate: 67.4, color: '#10b981' },  // Greece - Green

                      // Eastern Europe - Good win rates
                      '616': { rate: 65.3, color: '#10b981' },  // Poland - Green
                      '203': { rate: 64.8, color: '#10b981' },  // Czech Republic - Green
                      '348': { rate: 63.5, color: '#10b981' },  // Hungary - Green
                      '642': { rate: 62.1, color: '#10b981' },  // Romania - Green

                      // Asia - Mixed rates
                      '392': { rate: 48.5, color: '#3b82f6' },  // Japan - Blue
                      '410': { rate: 51.2, color: '#10b981' },  // South Korea - Green
                      '702': { rate: 46.9, color: '#3b82f6' },  // Singapore - Blue
                      '344': { rate: 43.7, color: '#3b82f6' },  // Hong Kong - Blue
                      '158': { rate: 39.8, color: '#f97316' },  // Taiwan - Orange
                      '764': { rate: 37.2, color: '#f97316' },  // Thailand - Orange
                      '458': { rate: 41.5, color: '#3b82f6' },  // Malaysia - Blue
                      '356': { rate: 44.3, color: '#3b82f6' },  // India - Blue

                      // Oceania - Lower rates
                      '036': { rate: 38.1, color: '#f97316' },  // Australia - Orange
                      '554': { rate: 43.8, color: '#3b82f6' },  // New Zealand - Blue

                      // Middle East
                      '784': { rate: 52.6, color: '#10b981' },  // UAE - Green
                      '376': { rate: 48.4, color: '#3b82f6' },  // Israel - Blue
                      '792': { rate: 45.1, color: '#3b82f6' },  // Turkey - Blue

                      // South America
                      '076': { rate: 41.8, color: '#3b82f6' },  // Brazil - Blue
                      '032': { rate: 43.2, color: '#3b82f6' },  // Argentina - Blue
                      '152': { rate: 39.5, color: '#f97316' },  // Chile - Orange
                      '170': { rate: 38.9, color: '#f97316' },  // Colombia - Orange
                    };

                    const countryInfo = countryData[geo.id];
                    const fillColor = countryInfo ? countryInfo.color : '#e2e8f0';
                    const opacity = countryInfo ? 0.7 : 1;

                    return (
                      <Geography
                        key={geo.rsmKey}
                        geography={geo}
                        fill={fillColor}
                        fillOpacity={opacity}
                        stroke="#94a3b8"
                        strokeWidth={0.5}
                        style={{
                          default: { outline: 'none' },
                          hover: { outline: 'none', fill: countryInfo ? countryInfo.color : '#cbd5e1', fillOpacity: countryInfo ? 0.9 : 1 },
                          pressed: { outline: 'none' }
                        }}
                      />
                    );
                  })
                }
              </Geographies>
              </ZoomableGroup>
            </ComposableMap>
          </div>

          <div className="mt-4 flex items-center justify-center gap-8 text-sm">
            <div className="flex items-center gap-3">
              <div className="w-4 h-4 rounded-full bg-emerald-500"></div>
              <span className="text-slate-700 font-semibold">≥50%</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-4 h-4 rounded-full bg-blue-500"></div>
              <span className="text-slate-700 font-semibold">40-49%</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-4 h-4 rounded-full bg-orange-500"></div>
              <span className="text-slate-700 font-semibold">35-39%</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-4 h-4 rounded-full bg-red-500"></div>
              <span className="text-slate-700 font-semibold">&lt;35%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;