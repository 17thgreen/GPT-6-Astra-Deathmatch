"""Illustrative single-order economics. No fitted probabilities or virtual fills."""
import json,math
from pathlib import Path

def expected_net(reward_rate,loss_on_fill,horizon_hours,mean_fill_hours):
    """Constant reward rate until an exponential full losing fill or horizon.

    Unfilled orders are assumed cancelled at horizon with zero inventory loss.
    All filled inventory is assumed worthless. No replenishment. This stylized
    process is an assumption, never estimated from empty-side public tape.
    """
    if min(reward_rate,loss_on_fill,horizon_hours,mean_fill_hours)<0:raise ValueError('negative input')
    if horizon_hours==0:return 0.
    if mean_fill_hours==0:return -loss_on_fill
    if math.isinf(mean_fill_hours):return reward_rate*horizon_hours
    hit_probability=-math.expm1(-horizon_hours/mean_fill_hours)
    return (reward_rate*mean_fill_hours-loss_on_fill)*hit_probability

def main():
    # Frozen AMS-009 campaign duration, used only as an illustrative parameter.
    duration_minutes=57.7170775
    reward_rate=100/(duration_minutes/60)*(1/3)*.5
    loss=11+1.1
    out={'designation':'unfitted theoretical sensitivity; no realized or simulated trading record',
         'assumptions':['One 1100-contract one-cent order; all inventory loses if fully filled.','Constant effective reward rate after competition and 50% qualifying time.','Time to a full losing fill follows an assumed exponential distribution.','No partial fills, replenishment, cancellation latency, or changing competition modelled.','Unfilled exposure ends without cost at the horizon; payout floors/eligibility omitted.','The $1.10 fee component is a chosen stress, not an actual venue fee.'],
         'horizon_minutes':duration_minutes,'effective_reward_per_hour':reward_rate,'loss_if_filled':loss,
         'break_even_mean_fill_minutes':loss/reward_rate*60,
         'cases':[{'assumed_mean_fill_minutes':m,'theoretical_expected_net':expected_net(reward_rate,loss,duration_minutes/60,m/60)} for m in (5,15,30,45,60,120)],
         'no_fill_ceiling':expected_net(reward_rate,loss,duration_minutes/60,math.inf)}
    p=Path(__file__).resolve().parent/'SURVIVAL_SENSITIVITY.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
