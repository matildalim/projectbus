const heatmapData = [
  {
    load: 'Light Load',
    gentle: { value: 0.80, status: 'optimal' },
    moderate: { value: 0.81, status: 'optimal' },
    aggressive: { value: 0.82, status: 'optimal' }
  },
  {
    load: 'Medium Load',
    gentle: { value: 0.88, status: 'optimal' },
    moderate: { value: 0.90, status: 'optimal' },
    aggressive: { value: 0.95, status: 'acceptable' }
  },
  {
    load: 'Heavy Load',
    gentle: { value: 0.98, status: 'optimal' },
    moderate: { value: 1.05, status: 'acceptable' },
    aggressive: { value: 1.15, status: 'wasteful' }
  }
];

function getCellColor(status: string) {
  switch (status) {
    case 'optimal':
      return 'bg-green-500';
    case 'acceptable':
      return 'bg-amber-500';
    case 'wasteful':
      return 'bg-red-500';
    default:
      return 'bg-gray-300';
  }
}

export function AccelerationHeatmap() {
  return (
    <div>
      {/* Heatmap Table */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr>
              <th className="border-2 border-gray-300 bg-gray-100 p-3 text-left text-gray-700">
                Load Category
              </th>
              <th className="border-2 border-gray-300 bg-gray-100 p-3 text-center text-gray-700">
                Gentle Accel
              </th>
              <th className="border-2 border-gray-300 bg-gray-100 p-3 text-center text-gray-700">
                Moderate Accel
              </th>
              <th className="border-2 border-gray-300 bg-gray-100 p-3 text-center text-gray-700">
                Aggressive Accel
              </th>
            </tr>
          </thead>
          <tbody>
            {heatmapData.map((row, rowIndex) => (
              <tr key={rowIndex}>
                <td className="border-2 border-gray-300 p-3 bg-gray-50 text-gray-900">
                  {row.load}
                </td>
                <td className="border-2 border-gray-300 p-0">
                  <div className={`${getCellColor(row.gentle.status)} text-white p-4 text-center`}>
                    <div className="text-2xl">{row.gentle.value}</div>
                    <div className="text-sm opacity-90">L/km</div>
                  </div>
                </td>
                <td className="border-2 border-gray-300 p-0">
                  <div className={`${getCellColor(row.moderate.status)} text-white p-4 text-center`}>
                    <div className="text-2xl">{row.moderate.value}</div>
                    <div className="text-sm opacity-90">L/km</div>
                  </div>
                </td>
                <td className={`border-2 border-gray-300 p-0 ${rowIndex === 2 ? 'border-4 border-red-700' : ''}`}>
                  <div className={`${getCellColor(row.aggressive.status)} text-white p-4 text-center relative`}>
                    <div className="text-2xl">{row.aggressive.value}</div>
                    <div className="text-sm opacity-90">L/km</div>
                    {rowIndex === 2 && (
                      <div className="absolute -top-2 -right-2 bg-red-700 text-white px-2 py-1 rounded text-xs">
                        17% PENALTY
                      </div>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Key Insight */}
      <div className="mt-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
        <div className="flex items-center gap-2">
          <div className="text-red-700 text-lg">
            🔴 <span className="ml-2">Key Insight:</span>
          </div>
        </div>
        <p className="text-red-800 mt-2">
          Heavy Load + Aggressive Acceleration = Highest fuel waste
        </p>
        <p className="text-red-600 text-sm mt-1">
          This combination accounts for the majority of preventable fuel consumption
        </p>
      </div>

      {/* Color Legend */}
      <div className="mt-4 flex gap-4 justify-center text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-green-500 rounded"></div>
          <span className="text-gray-700">Optimal</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-amber-500 rounded"></div>
          <span className="text-gray-700">Acceptable</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-red-500 rounded"></div>
          <span className="text-gray-700">Wasteful</span>
        </div>
      </div>
    </div>
  );
}
