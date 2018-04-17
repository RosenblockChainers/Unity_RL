using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CartPoleSampleAgent : Agent {

    [Header("Specific to Pole")]
    public GameObject pole;

    // Agentの観測を収集する．
    public override void CollectObservations()
    {
        float[] obs = new float[4];

        // 観測を計算
        // poleのx座標と速度
        obs[0] = this.transform.position.x;
        obs[1] = GetComponent<Rigidbody>().velocity.x;
        // poleのz軸中心の角度と角速度
        float angle = pole.transform.localEulerAngles.z;
        if (angle > 180.0f) {
            angle -= 360.0f;
        }
        obs[2] = angle * 2.0f * 3.14f / 360.0f;
        obs[3] = pole.GetComponent<Rigidbody>().angularVelocity.z;

        // 観測を収集
        for (int i = 0; i < obs.Length; ++i) {
            AddVectorObs(obs[i]);
        }

        // ログ出力
        Monitor.Log("Brain Type", brain.gameObject.name, MonitorType.text);
        Monitor.Log("Mode", brain.brainType, MonitorType.text);
        Monitor.Log("Reward", GetCumulativeReward(), MonitorType.text);
        Monitor.Log("Step Count", GetStepCount(), MonitorType.text);
        string obsText = "";
        for (int i = 0; i < obs.Length; ++i) {
            obsText += obs[i].ToString("F2") + " ";
        }
        Monitor.Log("observation", obsText, MonitorType.text);
    }

    // 入力が与えられたときにAgentが行うことを定義する．
    // 一般的な強化学習でいうと，行動を受け取って環境の更新を行う．
    // doneとrewardをセットする必要がある．
    public override void AgentAction(float[] vectorAction, string textAction)
	{
        float xThreshold = 2.4f;        // cartのx座標の閾値
        float thetaThreshold = 12.0f;   // poleの回転角度の閾値

        // 行動がセットされていたら，cartにx軸方向に力を加える．
        if (vectorAction[0] >= 0.0f) {
            GetComponent<Rigidbody>().AddForce(
                new Vector3((vectorAction[0] - 0.5f) * 20.0f, 0.0f, 0.0f)
            );
        }

        // 通常は+1ずつ報酬を与える．
        SetReward(1.0f);

        // doneとなって終了したら，報酬は与えない．
        // cartのx座標が範囲外に出ていたら，doneとして終了する．
        if (Mathf.Abs(this.transform.position.x) > xThreshold) {
            Done();
            SetReward(0.0f);
        }
        // poleが一定以上回転していたら，doneとして終了する．
        float angle = pole.transform.localEulerAngles.z;
        if (angle > 180.0f) {
            angle -= 360.0f;
        }
        if (Mathf.Abs(angle) > thetaThreshold) {
            Done();
            SetReward(0.0f);
        }
        
        // ログ出力
        Monitor.Log("action", vectorAction[0], MonitorType.text);
    }

    // Academyがリセットされたとき，もしくはAgentがdoneとなったときに呼び出される．
    // 一般的な強化学習でいうと，環境の初期化を行う．
    public override void AgentReset()
    {
        // cartの位置と速度を初期化．
        // x座標と速度のみ，微小な範囲からランダムに決定する．
        this.transform.position = new Vector3(Random.Range(-0.05f, 0.05f), 0f, 0f);
        GetComponent<Rigidbody>().velocity = new Vector3(Random.Range(-0.05f, 0.05f), 0f, 0f);

        // poleの位置と速度，角度と角速度を初期化．
        // z軸中心の角度と角速度のみ，微小な範囲からランダムに決定する．
        pole.transform.position = new Vector3(0.0f, 0.6f, 0.0f);
        pole.GetComponent<Rigidbody>().velocity = new Vector3(0f, 0f, 0f);
        pole.transform.rotation = new Quaternion(0f, 0f, 0f, 0f);
        pole.transform.Rotate(
            new Vector3(0, 0, 1),
            Random.Range(-0.05f, 0.05f) * 360.0f / (2.0f * 3.14f)
        );
        pole.GetComponent<Rigidbody>().angularVelocity =
            new Vector3(0f, 0f, Random.Range(-0.05f, 0.05f));
    }
}
