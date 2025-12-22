import { useState } from 'react';
import { OperationsDashboard } from './components/operations-dashboard';
import { DriverDisplay } from './components/driver-display';
import { BarChart3, Gauge } from 'lucide-react';
import { useData } from './context/DataContext';

export default function App() {
  const [activeInterface, setActiveInterface] = useState<'operations' | 'driver'>('operations');
  const { scenarioType, setScenarioType } = useData();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Interface Switcher */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex gap-4 mb-4">
            <button
              onClick={() => setActiveInterface('operations')}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-colors ${
                activeInterface === 'operations'
                  ? 'bg-blue-900 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <BarChart3 className="w-5 h-5" />
              Operations Dashboard
            </button>
            <button
              onClick={() => setActiveInterface('driver')}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-colors ${
                activeInterface === 'driver'
                  ? 'bg-blue-900 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Gauge className="w-5 h-5" />
              Driver Display
            </button>
          </div>

          {/* Demo Scenario Switcher */}
          <div className="flex gap-2 items-center">
            <span className="text-sm text-gray-600 mr-2">Demo Scenario:</span>
            <button
              onClick={() => setScenarioType('fleet')}
              className={`px-4 py-2 rounded text-sm transition-colors ${
                scenarioType === 'fleet'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Fleet View
            </button>
            <button
              onClick={() => setScenarioType('light')}
              className={`px-4 py-2 rounded text-sm transition-colors ${
                scenarioType === 'light'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Light Load Trip
            </button>
            <button
              onClick={() => setScenarioType('optimal')}
              className={`px-4 py-2 rounded text-sm transition-colors ${
                scenarioType === 'optimal'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Heavy Load (Optimal)
            </button>
            <button
              onClick={() => setScenarioType('wasteful')}
              className={`px-4 py-2 rounded text-sm transition-colors ${
                scenarioType === 'wasteful'
                  ? 'bg-red-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Heavy Load (WASTEFUL) ⚠️
            </button>
          </div>
        </div>
      </div>

      {/* Active Interface */}
      {activeInterface === 'operations' ? <OperationsDashboard /> : <DriverDisplay />}
    </div>
  );
}