import { LoadImpactChart } from './load-impact-chart';
import { AccelerationHeatmap } from './acceleration-heatmap';
import { SavingsCard } from './savings-card';
import { DriverLeaderboard } from './driver-leaderboard';
import { Calendar } from 'lucide-react';
import { useData } from '../context/DataContext';

export function OperationsDashboard() {
  const { fleetData, currentScenario, scenarioType, isLoading } = useData();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading data...</div>
      </div>
    );
  }

  // Use scenario data if viewing a specific trip, otherwise use fleet data
  const displayData = currentScenario || fleetData;
  
  // Extract stats based on what data we have
  const totalTrips = fleetData?.total_trips || 1;
  const fuelWaste = currentScenario 
    ? currentScenario.savings?.total_wasted_fuel || 0
    : fleetData?.fleet_savings?.weekly_fuel_waste || 0;

  const headerTitle = currentScenario 
    ? `Trip Analysis - ${currentScenario.trip_id}`
    : 'SmartDrive Analytics - Route 12';

  const quickStats = currentScenario
    ? `${currentScenario.load?.max_passenger_count || 0} passengers | ${fuelWaste.toFixed(1)}L wasted`
    : `${totalTrips} trips analyzed | ${fuelWaste.toFixed(1)}L fuel waste identified`;

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-[1920px] mx-auto">
        {/* Header */}
        <div className="bg-blue-900 text-white rounded-lg p-6 mb-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl mb-2">{headerTitle}</h1>
              <div className="flex items-center gap-2 text-blue-100">
                <Calendar className="w-5 h-5" />
                <span className="text-lg">Week of Dec 16-20, 2024</span>
              </div>
            </div>
            <div className="text-right">
              <div className="text-lg text-blue-100">Quick Stats</div>
              <div className="text-2xl mt-1">{quickStats}</div>
            </div>
          </div>
        </div>

        {/* Scenario Alert for Wasteful Trip */}
        {scenarioType === 'wasteful' && currentScenario && (
          <div className="bg-red-50 border-l-4 border-red-600 p-4 mb-6 rounded">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-600" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">⚠️ PROBLEM SCENARIO</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{currentScenario.savings?.main_issue}</p>
                  <p className="mt-1 font-semibold">
                    Wasted: {currentScenario.savings?.total_wasted_fuel}L (${currentScenario.savings?.total_wasted_cost}) - 
                    {currentScenario.savings?.waste_percentage}% fuel penalty
                  </p>
                  <p className="mt-2 text-red-900 font-bold">
                    → Solution: {currentScenario.savings?.main_action}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Main Grid - 2x2 layout */}
        <div className="grid grid-cols-2 gap-6">
          {/* Panel 1 - Load Impact Analysis */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl mb-4 text-gray-900">Load Impact Analysis</h2>
            <LoadImpactChart />
          </div>

          {/* Panel 2 - Acceleration Impact Matrix */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl mb-4 text-gray-900">Acceleration Impact Matrix</h2>
            <AccelerationHeatmap />
          </div>

          {/* Panel 3 - Savings Opportunity */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl mb-4 text-gray-900">Savings Opportunity</h2>
            <SavingsCard />
          </div>

          {/* Panel 4 - Driver Performance Leaderboard */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl mb-4 text-gray-900">Driver Performance Leaderboard</h2>
            <DriverLeaderboard />
          </div>
        </div>
      </div>
    </div>
  );
}