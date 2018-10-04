use_bpm 128 #this is stored in variable current_bpm

drumkit = {
  "bass"   => { 1 => :drum_bass_hard },
  "snare"  => { 1 => :drum_snare_hard },
  "hihat"  => { 1 => :drum_cymbal_closed,
                2 => :drum_cymbal_open }
}

drum_sheet_resolution = 0.25  #measuered in quarter notes (beats)
drum_sheet = {
  "bass"  => [1,0,0,0,0,0,0,0, 1,0,0,0,0,0,0,0, 1,0,0,0,0,0,0,0, 1,0,0,0,0,0,0,0].ring,
  "snare" => [0,0,0,0,1,0,0,0, 0,0,0,0,1,0,0,0, 0,0,0,0,1,0,0,0, 0,0,0,0,1,0,0,0].ring,
  "hihat" => [1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1].ring
}

live_loop :drums do
  beat = tick
  drum_sheet.each do |staff|
    instrument = staff[0]
    note = staff[1][beat]
    if (note != 0)
      #with_fx :sound_out do
      sample drumkit[instrument][note]
      #end
    end
  end
  sleep drum_sheet_resolution
end

live_loop :bass do
  use_synth :piano
  with_fx :sound_out, output: 10 ,amp: 0 do
    sync :drums
    play :a4
  end
end
