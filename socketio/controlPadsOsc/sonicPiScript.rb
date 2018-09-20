#to be used with the controlPadsOsc python script
#use rings for this reason: https://in-thread.sonic-pi.net/t/set-one-element-in-array/497/2
set :pad_enabled, (ring false, false, false, false, false)
set :pad_active, (ring false, false, false, false, false)
set :pad_text, (ring 'PAD 1', 'PAD 2', 'PAD 3', 'PAD 4', 'PAD 5')

#set the port to whatever the python script is listening to
use_osc "localhost", 5005

#helper functions
define :send_pad_status do
  osc '/pad_text',get[:pad_text]
  osc '/pad_enabled',get[:pad_enabled]
  osc '/pad_active',get[:pad_active]
end

define :set_pad_enabled do |i, status|
  set :pad_enabled, get[:pad_enabled].put(i,status)
  send_pad_status
end

define :set_pad_active do |i, status|
  set :pad_active, get[:pad_active].put(i,status)
  send_pad_status
end

define :set_pad_text do |i, text|
  set :pad_text, get[:pad_text].put(i, text)
  send_pad_status
end

#only play if pad is enabled and active
define :play_loop do |pad|
  return get[:pad_active][pad]
end

#listen for pad hits and toggle the active flag
live_loop :toggle_active do
  use_real_time
  i = (sync "/osc:127.0.0.1:**/pad")[0] #get pad index
  #only toggle if pad is enabled
  if (get[:pad_enabled][i])
    set :pad_active, get[:pad_active].put(i,!get[:pad_active][i]) #put creates a new ring
  end
  send_pad_status
end

#set these so they will be set when running the buffer
#enabled allows remote triggering by osc
set_pad_enabled 0, false
set_pad_enabled 1, false
set_pad_enabled 2, false
set_pad_enabled 3, false
set_pad_enabled 4, false
#setting a pad active will play the live loop
set_pad_active 0, false
set_pad_active 1, false
set_pad_active 2, false
set_pad_active 3, false
set_pad_active 4, false
#strings that show up on the remote buttons
set_pad_text 0, 'PAD 0'
set_pad_text 1, 'PAD 1'
set_pad_text 2, 'PAD 2'
set_pad_text 3, 'PAD 3'
set_pad_text 4, 'PAD 4'
#send the osc messages to update the remote
send_pad_status

#
# actual fun below! Paste this in a different buffer
#

#pad 0: drum beat!
live_loop :drumbeat do
  use_sched_ahead_time 0.1 #small delay to save on resources
  set_pad_enabled 0, true
  set_pad_text 0, 'BEAT'
  if (play_loop 0)
    sample :loop_amen, beat_stretch: 2
    sleep 2
  else
    sleep 0.1
  end
end

live_loop :bass do
  set_pad_enabled 1, true
  set_pad_text 1, 'BASS'
  sync :drumbeat
  use_synth :chipbass
  if (play_loop 1)
    play 50
  end
  sleep 0.5
end

