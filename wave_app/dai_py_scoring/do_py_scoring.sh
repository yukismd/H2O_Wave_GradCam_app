#!/bin/bash

echo "****** ****** do_py_scoring.sh START ****** ******"

echo "Model path" $1
echo "Input data path" $2
echo "Output data path" $3
echo "Output data path (grad cam)" $4

#export DRIVERLESS_AI_LICENSE_KEY="e5Ztkmpoe6ozWFc1uzYT5tWBIioBa2ht_gIdFARM_vpAWDljLnKSlHwZIK35Esrd1ExjWTHCqxAtMXdLV12SQwDnMWb6o9vM3xsnGAfP5WBEK1Lo6fxRfVCdoeR6e_y1vu1bHsH1vCfhkJnK_DzhE4LiSYQFz1MYUD4PIq2Xc8zcwjKJC5GMI_vyL9uod0zdvn6AfCkH3Sp3ZxGXbAAQOzjm0_cSPBPpbojqqkYHEDLf_qBHnj5ZKxmuVQU8nSEp2ZycSbYbYZy5KIrxCmr0HvFtw-C7JC_g1_JRpwCtmo6octYuefQ0huJx25bT-JDViT33-KzCyyjAauych0U4SmxpY2Vuc2VfdmVyc2lvbjoxCnNlcmlhbF9udW1iZXI6MwpsaWNlbnNlZV9vcmdhbml6YXRpb246SDJPLmFpCmxpY2Vuc2VlX2VtYWlsOnRvbWtAaDJvLmFpCmxpY2Vuc2VlX3VzZXJfaWQ6Mwppc19oMm9faW50ZXJuYWxfdXNlOnRydWUKY3JlYXRlZF9ieV9lbWFpbDp0b21rQGgyby5haQpjcmVhdGlvbl9kYXRlOjIwMjAvMTIvMTYKcHJvZHVjdDpEcml2ZXJsZXNzQUkKbGljZW5zZV90eXBlOmRldmVsb3BlcgpleHBpcmF0aW9uX2RhdGU6MjAyMS8xMi8zMQo="

# scoring-pipeline内Python仮想環境から実行
$1/scoring-pipeline/env/bin/python $HOME/H2O_Wave_GradCam_app/wave_app/dai_py_scoring/run_gradcam.py $1 $2 $3 $4

#echo {$1}/scoring-pipeline/env/bin/python

echo "****** ****** do_py_scoring.sh END ****** ******"
