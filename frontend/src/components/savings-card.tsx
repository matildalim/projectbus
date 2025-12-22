import { TrendingDown, DollarSign, AlertTriangle } from 'lucide-react';
import { useData } from '../context/DataContext';

export function SavingsCard() {
  const { fleetData, currentScenario, scenarioType } = useData();

  // Determine what data to show
  if (scenarioType === 'fleet' && fleetData) {
    // Fleet-wide view
    const savings = fleetData.fleet_savings;
    const projection = fleetData.sbs_fleet_projection;

    return (
      <div className="space-y-6">
        {/* Weekly Waste */}
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-6 h-6 text-red-600 flex-shrink-0 mt-1" />
            <div className="flex-1">
              <h3 className="text-2xl font-bold text-red-900">
                {savings?.weekly_fuel_waste?.toFixed(1) || 0}L
              </h3>
              <p className="text-sm text-red-700">Weekly Fuel Waste</p>
              <p className="text-lg font-semibold text-red-800 mt-1">
                ${savings?.weekly_cost_waste?.toFixed(2) || 0} SGD/week
              </p>
            </div>
          </div>
        </div>

        {/* Annual Route 12 */}
        <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <TrendingDown className="w-6 h-6 text-orange-600 flex-shrink-0 mt-1" />
            <div className="flex-1">
              <h3 className="text-2xl font-bold text-orange-900">
                ${savings?.annual_cost_waste?.toLocaleString() || 0}
              </h3>
              <p className="text-sm text-orange-700">Annual Cost (Route 12)</p>
              <p className="text-xs text-orange-600 mt-1">
                {savings?.annual_fuel_waste?.toFixed(0) || 0}L wasted annually
              </p>
            </div>
          </div>
        </div>

        {/* Fleet-Wide Projection */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <DollarSign className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
            <div className="flex-1">
              <h3 className="text-3xl font-bold text-blue-900">
                ${(projection?.projected_annual_cost_waste || 0).toLocaleString()}
              </h3>
              <p className="text-sm text-blue-700 font-semibold">
                Fleet-Wide Potential (3,300 buses)
              </p>
              <p className="text-xs text-blue-600 mt-1">
                {(projection?.projected_annual_fuel_waste || 0).toLocaleString()}L annually
              </p>
            </div>
          </div>
        </div>

        {/* Breakdown */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-3">Breakdown:</h4>
          <ul className="space-y-2 text-sm text-gray-700">
            <li className="flex justify-between">
              <span>• Heavy-load trips:</span>
              <span className="font-semibold">
                {fleetData.by_load_category?.HEAVY?.count || 0} ({fleetData.by_load_category?.HEAVY?.percentage || 0}%)
              </span>
            </li>
            <li className="flex justify-between">
              <span>• Trips with waste:</span>
              <span className="font-semibold">{savings?.trips_with_waste || 0}</span>
            </li>
            <li className="flex justify-between">
              <span>• Avg waste per trip:</span>
              <span className="font-semibold">{savings?.avg_waste_per_trip?.toFixed(2) || 0}L</span>
            </li>
          </ul>
        </div>

        {/* Action Button */}
        <button className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors">
          Generate Driver Training Report
        </button>
      </div>
    );
  } else if (currentScenario) {
    // Single trip view
    const savings = currentScenario.savings;

    return (
      <div className="space-y-6">
        {/* Trip Waste */}
        <div className={`border rounded-lg p-4 ${
          savings?.priority === 'CRITICAL' 
            ? 'bg-red-50 border-red-200' 
            : 'bg-yellow-50 border-yellow-200'
        }`}>
          <div className="flex items-start gap-3">
            <AlertTriangle className={`w-6 h-6 flex-shrink-0 mt-1 ${
              savings?.priority === 'CRITICAL' ? 'text-red-600' : 'text-yellow-600'
            }`} />
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <span className={`px-2 py-1 rounded text-xs font-bold ${
                  savings?.priority === 'CRITICAL' 
                    ? 'bg-red-600 text-white' 
                    : 'bg-yellow-600 text-white'
                }`}>
                  {savings?.priority}
                </span>
              </div>
              <h3 className="text-3xl font-bold text-gray-900">
                {savings?.total_wasted_fuel?.toFixed(2) || 0}L
              </h3>
              <p className="text-sm text-gray-700">Fuel Wasted This Trip</p>
              <p className="text-xl font-semibold text-gray-800 mt-1">
                ${savings?.total_wasted_cost?.toFixed(2) || 0} SGD
              </p>
              <p className="text-lg font-bold text-red-600 mt-2">
                {savings?.waste_percentage?.toFixed(1) || 0}% Fuel Penalty
              </p>
            </div>
          </div>
        </div>

        {/* Issue */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-2">Issue:</h4>
          <p className="text-sm text-gray-700">{savings?.main_issue}</p>
        </div>

        {/* Recommendation */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <h4 className="font-semibold text-green-900 mb-2">💡 Recommendation:</h4>
          <p className="text-sm text-green-800 font-medium">{savings?.main_action}</p>
        </div>

        {/* Segments Affected */}
        {savings?.heavy_aggressive_segments > 0 && (
          <div className="bg-red-50 rounded-lg p-4">
            <h4 className="font-semibold text-red-900 mb-2">Affected Segments:</h4>
            <p className="text-sm text-red-700">
              <span className="text-2xl font-bold">{savings.heavy_aggressive_segments}</span> segments
              with HEAVY load + AGGRESSIVE acceleration
            </p>
            <p className="text-sm text-red-600 mt-1">
              Total waste from these segments: {savings?.heavy_aggressive_waste?.toFixed(2)}L
            </p>
          </div>
        )}
      </div>
    );
  }

  return <div className="text-gray-500">No data available</div>;
}