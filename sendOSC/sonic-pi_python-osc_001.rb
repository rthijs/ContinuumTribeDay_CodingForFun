live_loop :testOSC do
  use_real_time
  n = (sync "/osc:127.0.0.1:**/filter")[0] #sync gets an array of values, take the first one
  print n
  play toMidiRange(n)
  sleep 1
end

define :toMidiRange do |input|
  midiRangeValue = 127 * input
  return midiRangeValue
end