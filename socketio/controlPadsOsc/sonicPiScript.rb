#to be used with the controlPadsOsc python script
#use rings for this reason: https://in-thread.sonic-pi.net/t/set-one-element-in-array/497/2
set :pad_enabled, (ring false, false, false, false, false)
set :pad_active, (ring false, false, false, false, false)
set :pad_text, (ring 'PAD 1', 'PAD 2', 'PAD 3', 'PAD 4', 'PAD 5')

#set the port to whatever the python script is listening to
use_osc "localhost", 5005

#only play if pad is enabled and active
define :play_loop do |pad|
  if (get[:pad_enabled][pad] and get[:pad_active][pad])
    return true
  else
    return false
  end
end

define :set_pad_enabled do |i, status|
  set :pad_enabled, get[:pad_enabled].put(i,status)
end

define :set_pad_text do |i, text|
  set :pad_text, get[:pad_text].put(i, text)
end

live_loop :toggle_active do
  use_real_time
  i = (sync "/osc:127.0.0.1:**/pad")[0] #get pad index
  set :pad_active, get[:pad_active].put(i,!get[:pad_active][i]) #put creates a new ring
end

live_loop :master do
  use_real_time
  osc '/sonicpitest',get[:pad_text]
  osc '/sonicpitest',get[:pad_enabled]
  osc '/sonicpitest',get[:pad_active]
  sleep 1
end