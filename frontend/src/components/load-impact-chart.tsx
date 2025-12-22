import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import { useData } from '../context/DataContext';

interface ChartDataPoint {
  category: string;
  'Actual Fuel': number;
  'Optimal': number;
  trips?: number;
  penalty?: string;
}

export function LoadImpactChart() {
  const { fleetData, currentScenario, scenarioType } = useData();

  // Prepare data based on scenario
  let chartData: ChartDataPoint[] = [];

  if (scenarioType === 'fleet' && fleetData) {
    // Fleet-wide data
    const byLoad = fleetData.by_load_category || {};
    
    chartData = [
      {
        category: 'Light Load\n(<30 pax)',
        'Actual Fuel': byLoad.LIGHT?.avg_fuel_per_km || 0,
        'Optimal': 0.80,
        trips: byLoad.LIGHT?.count || 0
      },
      {
        category: 'Medium Load\n(31-60 pax)',
        'Actual Fuel': byLoad.MEDIUM?.avg_fuel_per_km || 0,
        'Optimal': 0.88,
        trips: byLoad.MEDIUM?.count || 0
      },
      {
        category: 'Heavy Load\n(61+ pax)',
        'Actual Fuel': byLoad.HEAVY?.avg_fuel_per_km || 0,
        'Optimal': 0.98,
        trips: byLoad.HEAVY?.count || 0
      }
    ];
  } else if (currentScenario) {
    // Single trip - show dominant load
    const loadCat = currentScenario.load?.dominant_load_category || 'MEDIUM';
    const fuelRate = currentScenario.fuel?.avg_fuel_per_km || 0;
    
    const optimalRates: { [key: string]: number } = { 
      'LIGHT': 0.80, 
      'MEDIUM': 0.88, 
      'HEAVY': 0.98 
    };
    const optimal = optimalRates[loadCat] || 0.88;

    chartData = [
      {
        category: `${loadCat} Load`,
        'Actual Fuel': fuelRate,
        'Optimal': optimal,
        penalty: ((fuelRate - optimal) / optimal * 100).toFixed(1)
      }
    ];
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <p className="text-sm text-gray-600">Fuel Consumption by Load Category (L/km)</p>
        {scenarioType === 'fleet' && (
          <div className="text-xs text-gray-500">
            Total trips: {fleetData?.total_trips || 0}
          </div>
        )}
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis 
            dataKey="category" 
            tick={{ fontSize: 12 }}
            angle={0}
            textAnchor="middle"
          />
          <YAxis 
            label={{ value: 'Fuel (L/km)', angle: -90, position: 'insideLeft' }}
            domain={[0, 1.2]}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc' }}
            formatter={(value: any) => `${Number(value).toFixed(3)} L/km`}
          />
          <Legend />
          <ReferenceLine y={0.98} stroke="#22c55e" strokeDasharray="3 3" label="Optimal (Heavy)" />
          <Bar dataKey="Optimal" fill="#22c55e" name="Optimal (Gentle)" />
          <Bar dataKey="Actual Fuel" fill="#ef4444" name="Actual" />
        </BarChart>
      </ResponsiveContainer>

      {/* Stats below chart */}
      <div className="grid grid-cols-3 gap-4 text-sm">
        {chartData.map((item, idx) => (
          <div key={idx} className="bg-gray-50 p-3 rounded">
            <div className="font-semibold text-gray-900">{item.category}</div>
            {item.trips !== undefined && (
              <div className="text-xs text-gray-600">{item.trips} trips</div>
            )}
            {item.penalty !== undefined && parseFloat(item.penalty) > 5 && (
              <div className="text-red-600 font-bold mt-1">+{item.penalty}% penalty</div>
            )}
          </div>
        ))}
      </div>

      {scenarioType === 'wasteful' && currentScenario && (
        <div className="bg-red-50 border border-red-200 rounded p-3 text-sm">
          <p className="text-red-900 font-semibold">
            ⚠️ Heavy load driven aggressively wastes {currentScenario.savings?.waste_percentage || 0}% fuel
          </p>
          <p className="text-red-700 mt-1">
            Switching to gentle acceleration would save {currentScenario.savings?.total_wasted_fuel || 0}L per trip
          </p>
        </div>
      )}
    </div>
  );
}