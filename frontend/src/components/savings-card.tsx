import { TrendingDown, DollarSign, AlertTriangle } from 'lucide-react';

export function SavingsCard() {
  return (
    <div className="space-y-6">
      {/* Main Savings Display */}
      <div className="bg-red-50 border-2 border-red-400 rounded-lg p-6 text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <AlertTriangle className="w-8 h-8 text-red-600" />
          <div className="text-gray-700 text-lg">Weekly Fuel Waste</div>
        </div>
        <div className="text-6xl text-red-600 mb-2">220.5 L</div>
      </div>

      {/* Cost Impact Cards */}
      <div className="grid grid-cols-1 gap-4">
        <div className="bg-gradient-to-r from-amber-50 to-amber-100 border border-amber-300 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-gray-700 text-sm">Cost Impact</div>
              <div className="text-3xl text-amber-900">$330.75</div>
              <div className="text-gray-600 text-sm">SGD/week</div>
            </div>
            <DollarSign className="w-12 h-12 text-amber-600" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-orange-50 to-orange-100 border border-orange-300 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-gray-700 text-sm">Annual Potential</div>
              <div className="text-3xl text-orange-900">$17,199</div>
              <div className="text-gray-600 text-sm">Single route savings</div>
            </div>
            <TrendingDown className="w-12 h-12 text-orange-600" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-red-50 to-red-100 border border-red-300 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-gray-700 text-sm">Fleet-Wide Impact</div>
              <div className="text-3xl text-red-900">$2.18M</div>
              <div className="text-gray-600 text-sm">Per year across fleet</div>
            </div>
            <TrendingDown className="w-12 h-12 text-red-600" />
          </div>
        </div>
      </div>

      {/* Breakdown List */}
      <div className="bg-gray-50 rounded-lg p-4 space-y-3">
        <div className="text-gray-700 mb-3">Waste Breakdown</div>
        
        <div className="flex items-center justify-between border-b border-gray-200 pb-2">
          <span className="text-gray-700">Heavy load trips</span>
          <span className="text-gray-900">147 <span className="text-gray-500">(35%)</span></span>
        </div>
        
        <div className="flex items-center justify-between border-b border-gray-200 pb-2">
          <span className="text-gray-700">Trips with aggressive accel</span>
          <span className="text-gray-900">88 <span className="text-gray-500">(60% of heavy loads)</span></span>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-gray-700">Average waste per trip</span>
          <span className="text-red-600">1.5 L</span>
        </div>
      </div>

      {/* Action Button */}
      <button className="w-full bg-blue-900 text-white py-4 rounded-lg hover:bg-blue-800 transition-colors">
        Generate Driver Training Report
      </button>
    </div>
  );
}
