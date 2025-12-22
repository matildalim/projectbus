import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';

const data = [
  {
    name: 'Light Load\n(<30 pax)',
    actual: 0.81,
    optimal: 0.80,
    fill: '#10b981'
  },
  {
    name: 'Medium Load\n(31-60 pax)',
    actual: 0.92,
    optimal: 0.88,
    fill: '#f59e0b'
  },
  {
    name: 'Heavy Load\n(61+ pax)',
    actual: 1.08,
    optimal: 0.98,
    fill: '#ef4444'
  }
];

export function LoadImpactChart() {
  return (
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="name" 
            tick={{ fill: '#374151' }}
            interval={0}
          />
          <YAxis 
            label={{ value: 'Fuel Consumption (L/km)', angle: -90, position: 'insideLeft', fill: '#374151' }}
            domain={[0, 1.2]}
            tick={{ fill: '#374151' }}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          <Bar dataKey="actual" name="Actual Consumption" fill="#1e3a8a" radius={[8, 8, 0, 0]} />
          {data.map((entry, index) => (
            <ReferenceLine
              key={index}
              y={entry.optimal}
              stroke="#9ca3af"
              strokeDasharray="5 5"
              strokeWidth={2}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>

      {/* Callout and Stats */}
      <div className="mt-6 space-y-3">
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
          <p className="text-red-800">
            <span className="font-bold">Heavy loads 10% above optimal</span>
          </p>
          <p className="text-red-600 text-sm mt-1">Dotted lines indicate optimal fuel consumption rates</p>
        </div>
        
        <div className="flex items-center justify-between bg-gray-50 p-4 rounded-lg">
          <div>
            <div className="text-gray-600 text-sm">Heavy-Load Trips</div>
            <div className="text-2xl text-gray-900">147</div>
          </div>
          <div className="text-right">
            <div className="text-gray-600 text-sm">Percentage of Total</div>
            <div className="text-2xl text-gray-900">35%</div>
          </div>
        </div>
      </div>
    </div>
  );
}
