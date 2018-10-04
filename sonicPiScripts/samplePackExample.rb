samples = "/home/roel/Music/samples/**"

use_bpm 140

live_loop :foo do
  sample samples, "140", "Cm",  20, beat_stretch: 32
  sleep 32
end

live_loop :bar do
  32.times do
    play :c1
    play :c2
    sleep 1
  end
end

with_fx :echo do
  live_loop :bleeps do
    use_random_seed 14
    32.times do
      play (ring :gb2, :eb2, :ab2, :bb2).choose, amp: rrand(20,50)/100
      sleep 1
    end
  end
end

with_fx :reverb, room: 1 do
  live_loop :melody do
    sync :foo
    use_synth :dark_ambience
    play_pattern_timed (chord :eb3, :major),[5,7,5], amp: 0.5, env_curve: 3
  end
end

with_fx :reverb, room: 1 do
  with_fx :echo do
    live_loop :weirdshit do
      sync :foo
      sample samples, "DNF_140_E_On_Edge", 1, rate: 1, amp: 0.6
      sleep 16
      sample samples, "DNF_140_E_On_Edge", 1, rate: -1, amp: 0.6
    end
  end
end



