import { TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react';

const driverData = [
  { rank: 1, name: 'Driver Wei', efficiency: 0.99, vsAvg: -8.3, medal: '🥇' },
  { rank: 2, name: 'Driver Priya', efficiency: 1.01, vsAvg: -6.5, medal: '🥈' },
  { rank: 3, name: 'Driver Raj', efficiency: 1.04, vsAvg: -3.7, medal: '🥉' },
  { rank: 4, name: 'Driver Sarah', efficiency: 1.07, vsAvg: -0.9, medal: '' },
  { rank: 5, name: 'Driver Chen', efficiency: 1.09, vsAvg: 0.9, medal: '' },
  { rank: 6, name: 'Driver Kumar', efficiency: 1.10, vsAvg: 1.9, medal: '' },
  { rank: 7, name: 'Driver Ahmad', efficiency: 1.12, vsAvg: 3.7, medal: '' },
  { rank: 8, name: 'Driver Lee', efficiency: 1.18, vsAvg: 9.3, medal: '' }
];

function getRowClass(rank: number) {
  if (rank <= 3) return 'bg-green-50 border-l-4 border-green-500';
  if (rank >= 7) return 'bg-red-50 border-l-4 border-red-500';
  if (rank >= 6) return 'bg-amber-50 border-l-4 border-amber-500';
  return 'bg-white';
}

function getPerformanceIcon(vsAvg: number) {
  if (vsAvg < 0) return <TrendingDown className="w-4 h-4 text-green-600 inline" />;
  if (vsAvg > 5) return <AlertTriangle className="w-4 h-4 text-red-600 inline" />;
  return <TrendingUp className="w-4 h-4 text-amber-600 inline" />;
}

function getVsAvgText(vsAvg: number) {
  const sign = vsAvg > 0 ? '+' : '';
  const color = vsAvg < 0 ? 'text-green-600' : vsAvg > 5 ? 'text-red-600' : 'text-amber-600';
  const symbol = vsAvg < 0 ? '✓' : vsAvg > 5 ? '🔴' : '⚠';
  
  return (
    <span className={color}>
      {sign}{vsAvg.toFixed(1)}% {symbol}
    </span>
  );
}

export function DriverLeaderboard() {
  return (
    <div>
      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b-2 border-gray-300 bg-gray-50">
              <th className="text-left p-3 text-gray-700">Rank</th>
              <th className="text-left p-3 text-gray-700">Driver</th>
              <th className="text-right p-3 text-gray-700">Heavy Load Efficiency</th>
              <th className="text-right p-3 text-gray-700">vs Fleet Avg</th>
            </tr>
          </thead>
          <tbody>
            {driverData.map((driver) => (
              <tr 
                key={driver.rank}
                className={`${getRowClass(driver.rank)} border-b border-gray-200 transition-colors hover:opacity-80`}
              >
                <td className="p-3">
                  <div className="flex items-center gap-2">
                    {driver.medal && <span className="text-2xl">{driver.medal}</span>}
                    {!driver.medal && <span className="text-gray-600">{driver.rank}th</span>}
                  </div>
                </td>
                <td className="p-3">
                  <span className="text-gray-900">{driver.name}</span>
                </td>
                <td className="p-3 text-right">
                  <span className="text-gray-900">{driver.efficiency.toFixed(2)} L/km</span>
                </td>
                <td className="p-3 text-right">
                  <div className="flex items-center justify-end gap-1">
                    {getPerformanceIcon(driver.vsAvg)}
                    {getVsAvgText(driver.vsAvg)}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Footer */}
      <div className="mt-4 bg-blue-50 border-l-4 border-blue-900 p-4 rounded">
        <p className="text-blue-900">
          Fleet average: <span className="font-bold">1.08 L/km</span> on heavy loads
        </p>
        <p className="text-blue-700 text-sm mt-1">
          Top 3 drivers save an average of 6.2% compared to fleet baseline
        </p>
      </div>
    </div>
  );
}
