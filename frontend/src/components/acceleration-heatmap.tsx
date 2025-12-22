import { useData } from '../context/DataContext';

export function AccelerationHeatmap() {
  const { scenarioType } = useData();

  // Fuel consumption matrix (L/km) - from fuel_estimator.py
  const matrix = {
    'LIGHT': {
      'GENTLE': { fuel: 0.800, penalty: 0 },
      'MODERATE': { fuel: 0.810, penalty: 1.2 },
      'AGGRESSIVE': { fuel: 0.820, penalty: 2.5 }
    },
    'MEDIUM': {
      'GENTLE': { fuel: 0.880, penalty: 0 },
      'MODERATE': { fuel: 0.920, penalty: 4.5 },
      'AGGRESSIVE': { fuel: 0.945, penalty: 7.4 }
    },
    'HEAVY': {
      'GENTLE': { fuel: 0.980, penalty: 0 },
      'MODERATE': { fuel: 1.050, penalty: 7.1 },
      'AGGRESSIVE': { fuel: 1.150, penalty: 17.3 }
    }
  };

  const getColor = (load: string, accel: string) => {
    const data = matrix[load][accel];
    if (data.penalty === 0) return 'bg-green-100 border-green-300 text-green-900';
    if (data.penalty < 5) return 'bg-green-50 border-green-200 text-green-800';
    if (data.penalty < 10) return 'bg-yellow-100 border-yellow-300 text-yellow-900';
    return 'bg-red-100 border-red-400 text-red-900 font-bold';
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-600">
        Fuel consumption (L/km) by Load × Acceleration combination
      </p>

      {/* Heatmap Table */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr>
              <th className="border border-gray-300 bg-gray-100 p-2 text-sm font-semibold"></th>
              <th className="border border-gray-300 bg-green-50 p-2 text-sm font-semibold">
                Gentle<br/>
                <span className="text-xs font-normal">(&lt;1.5 m/s²)</span>
              </th>
              <th className="border border-gray-300 bg-yellow-50 p-2 text-sm font-semibold">
                Moderate<br/>
                <span className="text-xs font-normal">(1.5-2.5 m/s²)</span>
              </th>
              <th className="border border-gray-300 bg-red-50 p-2 text-sm font-semibold">
                Aggressive<br/>
                <span className="text-xs font-normal">(&gt;2.5 m/s²)</span>
              </th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(matrix).map(([load, accels]) => (
              <tr key={load}>
                <td className="border border-gray-300 bg-gray-100 p-2 text-sm font-semibold">
                  {load}<br/>
                  <span className="text-xs font-normal">
                    {load === 'LIGHT' && '(0-30 pax)'}
                    {load === 'MEDIUM' && '(31-60 pax)'}
                    {load === 'HEAVY' && '(61+ pax)'}
                  </span>
                </td>
                {Object.entries(accels).map(([accel, data]) => (
                  <td 
                    key={accel}
                    className={`border-2 p-3 text-center ${getColor(load, accel)}`}
                  >
                    <div className="text-lg font-bold">{data.fuel.toFixed(3)}</div>
                    {data.penalty > 0 && (
                      <div className="text-xs mt-1">+{data.penalty}%</div>
                    )}
                    {data.penalty === 0 && (
                      <div className="text-xs mt-1 text-green-600">✓ Optimal</div>
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Key Insight Box */}
      <div className="bg-blue-50 border-l-4 border-blue-600 p-4">
        <h4 className="font-semibold text-blue-900 mb-2">🔑 KEY INSIGHT:</h4>
        <div className="space-y-1 text-sm text-blue-800">
          <p>• Light load + Aggressive = <span className="font-bold">+2.5%</span> (minimal impact)</p>
          <p>• Medium load + Aggressive = <span className="font-bold">+7.4%</span> (moderate impact)</p>
          <p className="text-red-600 font-bold text-base">
            • Heavy load + Aggressive = <span className="text-xl">+17.3%</span> (CRITICAL!) ← THE PROBLEM
          </p>
        </div>
      </div>

      {scenarioType === 'wasteful' && (
        <div className="bg-red-50 border border-red-200 rounded p-3 text-sm">
          <p className="text-red-900 font-bold">
            ⚠️ Current scenario demonstrates this exact problem!
          </p>
          <p className="text-red-700 mt-1">
            Heavy bus (72 passengers) + Aggressive acceleration = 17% fuel waste
          </p>
        </div>
      )}
    </div>
  );
}