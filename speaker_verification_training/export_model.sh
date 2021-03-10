mkdir -p model/exp/xvector_nnet_1a/configs
mkdir -p model/exp/xvector_nnet_1a/xvectors_train

cd data/test
tar -cvzf trials.tgz trials
cd -

cp exp/xvector_nnet_1a/accuracy.output.report model/exp/xvector_nnet_1a/
cp exp/xvector_nnet_1a/configs/final.config model/exp/xvector_nnet_1a/configs/
cp exp/xvector_nnet_1a/configs/network.xconfig model/exp/xvector_nnet_1a/configs/
cp exp/xvector_nnet_1a/configs/ref.config model/exp/xvector_nnet_1a/configs/
cp exp/xvector_nnet_1a/configs/ref.raw model/exp/xvector_nnet_1a/configs/
cp exp/xvector_nnet_1a/configs/vars model/exp/xvector_nnet_1a/configs/
cp exp/xvector_nnet_1a/configs/xconfig model/exp/xvector_nnet_1a/configs/
cp exp/xvector_nnet_1a/configs/xconfig.expanded.1 model/exp/xvector_nnet_1a/configs/
cp exp/xvector_nnet_1a/configs/xconfig.expanded.2 model/exp/xvector_nnet_1a/configs/
cp exp/xvector_nnet_1a/extract.config model/exp/xvector_nnet_1a/
cp exp/xvector_nnet_1a/final.raw model/exp/xvector_nnet_1a/
cp exp/xvector_nnet_1a/max_chunk_size model/exp/xvector_nnet_1a/
cp exp/xvector_nnet_1a/min_chunk_size model/exp/xvector_nnet_1a/
cp exp/xvector_nnet_1a/nnet.config model/exp/xvector_nnet_1a/
cp exp/xvector_nnet_1a/srand model/exp/xvector_nnet_1a/
cp exp/xvector_nnet_1a/xvectors_train/mean.vec model/exp/xvector_nnet_1a/xvectors_train/
cp exp/xvector_nnet_1a/xvectors_train/num_utts.ark model/exp/xvector_nnet_1a/xvectors_train/
cp exp/xvector_nnet_1a/xvectors_train/plda model/exp/xvector_nnet_1a/xvectors_train/
cp exp/xvector_nnet_1a/xvectors_train/spk_xvector.ark model/exp/xvector_nnet_1a/xvectors_train/
cp exp/xvector_nnet_1a/xvectors_train/spk_xvector.scp model/exp/xvector_nnet_1a/xvectors_train/
cp exp/xvector_nnet_1a/xvectors_train/transform.mat model/exp/xvector_nnet_1a/xvectors_train/
cp exp/xvector_nnet_1a/xvectors_train/xvector.scp model/exp/xvector_nnet_1a/xvectors_train/
cp data/test/trials.tgz model/exp/xvector_nnet_1a/
