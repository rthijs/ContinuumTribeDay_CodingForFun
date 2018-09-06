set :flag_bass_drum, false

live_loop :toggle_bass_drum do
  use_real_time
  sync "/osc:127.0.0.1:35544/pad/A0"
  set :flag_bass_drum, (!get[:flag_bass_drum])
  print get[:flag_bass_drum]
end

live_loop :bass_drum do
  if get[:flag_bass_drum]
    sample :drum_bass_hard
  end
  sleep 1
end