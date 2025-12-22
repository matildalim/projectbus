import { LoadImpactChart } from './load-impact-chart';
import { AccelerationHeatmap } from './acceleration-heatmap';
import { SavingsCard } from './savings-card';
import { DriverLeaderboard } from './driver-leaderboard';
import { Calendar } from 'lucide-react';

export function OperationsDashboard() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-[1920px] mx-auto">
        {/* Header */}
        <div className="bg-blue-900 text-white rounded-lg p-6 mb-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl mb-2">SmartDrive Analytics - Route 12</h1>
              <div className="flex items-center gap-2 text-blue-100">
                <Calendar className="w-5 h-5" />
                <span className="text-lg">Week of Dec 16-20, 2024</span>
              </div>
            </div>
            <div className="text-right">
              <div className="text-lg text-blue-100">Quick Stats</div>
              <div className="text-2xl mt-1">420 trips analyzed | 220L fuel waste identified</div>
            </div>
          </div>
        </div>

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
