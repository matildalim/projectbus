import { useState } from 'react';
import { Users, MapPin, Gauge, TrendingDown, AlertTriangle, Circle } from 'lucide-react';

type LoadLevel = 'light' | 'medium' | 'heavy';

export function DriverDisplay() {
  const [loadLevel, setLoadLevel] = useState<LoadLevel>('heavy');
  const [currentAccel, setCurrentAccel] = useState(1.2);

  const loadConfigs = {
    light: {
      passengers: 22,
      capacity: 26,
      label: 'LIGHT LOAD',
      bgColor: 'bg-green-500',
      borderColor: 'border-green-500',
      message: 'Normal driving OK',
      guidance: 'Acceleration has minimal fuel impact',
      guidanceColor: 'bg-blue-50 border-blue-300',
      iconColor: 'text-blue-600',
      showPenalty: false
    },
    medium: {
      passengers: 48,
      capacity: 57,
      label: 'MEDIUM LOAD',
      bgColor: 'bg-amber-500',
      borderColor: 'border-amber-500',
      message: 'MODERATE ACCELERATION OPTIMAL',
      guidance: 'Avoid rapid acceleration to maintain efficiency',
      guidanceColor: 'bg-blue-100 border-blue-400',
      iconColor: 'text-blue-700',
      showPenalty: false
    },
    heavy: {
      passengers: 72,
      capacity: 86,
      label: 'HEAVY LOAD',
      bgColor: 'bg-red-500',
      borderColor: 'border-red-500',
      message: 'USE GENTLE ACCELERATION',
      guidance: 'Heavy bus weight increases fuel consumption significantly',
      guidanceColor: 'bg-amber-100 border-amber-400',
      iconColor: 'text-amber-600',
      showPenalty: true
    }
  };

  const config = loadConfigs[loadLevel];
  const isGoodAccel = currentAccel < 1.5;

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="w-full max-w-5xl bg-white rounded-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="bg-blue-900 text-white px-8 py-5 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div>
              <div className="text-sm text-blue-200">SmartDrive | Route 12</div>
              <div className="text-lg">Bus SBS5678T</div>
            </div>
          </div>
          <div className="flex items-center gap-6">
            <div className="text-right">
              <div className="text-sm text-blue-200">Current Time</div>
              <div className="text-3xl">07:26</div>
            </div>
            <div className="flex items-center gap-2">
              <Circle className="w-3 h-3 fill-green-400 text-green-400" />
              <span className="text-sm text-green-200">System Active</span>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="p-8 space-y-6">
          {/* Section 1 - Current Load Status */}
          <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl border-2 border-gray-300 p-8 text-center shadow-lg">
            <Users className="w-16 h-16 mx-auto mb-4 text-gray-700" />
            <div className="text-gray-600 text-sm tracking-wider mb-2">CURRENT LOAD</div>
            <div className="text-6xl text-gray-900 mb-3">{config.passengers} PASSENGERS</div>
            <div className="text-2xl text-gray-600 mb-6">{config.capacity}% capacity</div>
            <div className={`inline-block ${config.bgColor} text-white px-12 py-4 rounded-xl text-3xl shadow-lg animate-pulse`}>
              {config.label}
            </div>
          </div>

          {/* Section 2 - Acceleration Guidance */}
          <div className={`${config.guidanceColor} border-2 rounded-2xl p-8 shadow-lg`}>
            <div className="flex items-start gap-6">
              <AlertTriangle className={`w-12 h-12 ${config.iconColor} flex-shrink-0 mt-2`} />
              <div className="flex-1">
                <div className="text-4xl text-gray-900 mb-6">{config.message}</div>
                
                <div className={`${loadLevel === 'heavy' ? 'bg-amber-50' : 'bg-white'} rounded-xl p-6 space-y-3 border border-gray-200`}>
                  <div className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-gray-700 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-gray-800 text-lg">{config.guidance}</p>
                  </div>
                  
                  {config.showPenalty && (
                    <>
                      <div className="flex items-start gap-3">
                        <div className="w-2 h-2 bg-gray-700 rounded-full mt-2 flex-shrink-0"></div>
                        <p className="text-gray-800 text-lg">
                          <span className="text-red-600">Aggressive acceleration = 17% fuel penalty</span>
                        </p>
                      </div>
                      <div className="flex items-start gap-3">
                        <div className="w-2 h-2 bg-gray-700 rounded-full mt-2 flex-shrink-0"></div>
                        <p className="text-gray-800 text-lg">
                          <span className="text-green-600">Gentle throttle saves 2.5L this trip</span>
                        </p>
                      </div>
                    </>
                  )}
                </div>

                {/* Visual Aid - Accelerator Pedal */}
                {config.showPenalty && (
                  <div className="mt-6 bg-white rounded-xl p-6 border border-gray-200">
                    <div className="text-gray-700 text-lg mb-4">Accelerator Pedal Guidance</div>
                    <div className="flex gap-4">
                      <div className="flex-1 bg-green-100 border-2 border-green-500 rounded-lg p-4 text-center">
                        <div className="text-green-700 text-sm mb-2">✓ GRADUAL PRESSURE</div>
                        <div className="text-green-900">Smooth, steady increase</div>
                      </div>
                      <div className="flex-1 bg-red-100 border-2 border-red-500 rounded-lg p-4 text-center">
                        <div className="text-red-700 text-sm mb-2">✗ HARD PRESS</div>
                        <div className="text-red-900">Rapid acceleration</div>
                      </div>
                    </div>
                    <div className="mt-4 text-center text-gray-700 bg-gray-50 p-3 rounded-lg">
                      Target: <span className="text-blue-900">&lt;1.5 m/s²</span> acceleration
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Section 3 - Trip Info Bar */}
          <div className="grid grid-cols-3 gap-6 bg-gray-50 rounded-2xl p-6 border-2 border-gray-200">
            {/* Next Stop */}
            <div className="text-center">
              <MapPin className="w-10 h-10 mx-auto mb-3 text-blue-900" />
              <div className="text-gray-600 text-sm mb-1">Next Stop</div>
              <div className="text-xl text-gray-900">Bedok Interchange</div>
              <div className="text-gray-600">800m ahead</div>
            </div>

            {/* Current Performance */}
            <div className="text-center border-x-2 border-gray-300">
              <Gauge className="w-10 h-10 mx-auto mb-3 text-blue-900" />
              <div className="text-gray-600 text-sm mb-1">Current Performance</div>
              <div className={`text-xl ${isGoodAccel ? 'text-green-600' : 'text-red-600'}`}>
                Current: {currentAccel.toFixed(1)} m/s²
              </div>
              <div className={`${isGoodAccel ? 'text-green-600' : 'text-red-600'}`}>
                Status: {isGoodAccel ? '✓ Gentle' : '✗ Too Hard'}
              </div>
            </div>

            {/* Trip Savings */}
            <div className="text-center">
              <TrendingDown className="w-10 h-10 mx-auto mb-3 text-green-600" />
              <div className="text-gray-600 text-sm mb-1">Trip Savings</div>
              <div className="text-xl text-green-600">Fuel saved: 1.8L</div>
              <div className="text-green-700">Cost: $2.70 SGD</div>
            </div>
          </div>

          {/* Load Level Selector (for demo purposes) */}
          <div className="border-t-2 border-gray-200 pt-6">
            <div className="text-gray-600 text-sm mb-3 text-center">Demo Controls (not visible to driver)</div>
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => setLoadLevel('light')}
                className={`px-6 py-3 rounded-lg transition-colors ${
                  loadLevel === 'light' ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-700'
                }`}
              >
                Light Load
              </button>
              <button
                onClick={() => setLoadLevel('medium')}
                className={`px-6 py-3 rounded-lg transition-colors ${
                  loadLevel === 'medium' ? 'bg-amber-500 text-white' : 'bg-gray-200 text-gray-700'
                }`}
              >
                Medium Load
              </button>
              <button
                onClick={() => setLoadLevel('heavy')}
                className={`px-6 py-3 rounded-lg transition-colors ${
                  loadLevel === 'heavy' ? 'bg-red-500 text-white' : 'bg-gray-200 text-gray-700'
                }`}
              >
                Heavy Load
              </button>
            </div>
            <div className="flex gap-4 justify-center mt-3">
              <button
                onClick={() => setCurrentAccel(1.2)}
                className={`px-4 py-2 rounded text-sm transition-colors ${
                  currentAccel === 1.2 ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-700'
                }`}
              >
                Gentle (1.2 m/s²)
              </button>
              <button
                onClick={() => setCurrentAccel(2.1)}
                className={`px-4 py-2 rounded text-sm transition-colors ${
                  currentAccel === 2.1 ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-700'
                }`}
              >
                Aggressive (2.1 m/s²)
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
