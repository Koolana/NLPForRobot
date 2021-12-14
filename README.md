# Point Generation Network <br/> in the motion command recognition task <br/> for Russian language

The main goal is to implement a mechanism for robot recognition of systematized commands from unstructured sources, in particular, human speech.
The tasks we set for this project:
1. Make a dataset of possible sentences from a human to a robot, containing a veiled motion command, and target commands easily recognized by the robot.
2. Implement an encoder that will convert an incoming sequence containing a motion command into a context vector.
3. Implement a Point Generation Network (PGN)-based decoder to correctly fill the output command slots from the incoming sequence.

More details in the file **report/NLP_project.pdf**

## Getting Started

### Requirements

This project is based on **Python 3**, depends on the following libraries, and has been tested for version compatibility:

```
numpy==1.21.2
torch==1.10.0
transformers==4.13.0
tqdm==4.62.3
natasha==1.4.0
scikit-learn==0.24.2
torchtext==0.11.0
```

Also, the project uses a tokenizer from the model [ruRoberta](https://huggingface.co/sberbank-ai/ruRoberta-large). This model must be downloaded and moved into **models** folder. 

### Installing

```
git clone https://github.com/Koolana/NLPForRobot.git
```

## Launch

Scripts for launching and testing are located in the **src** folder, further instructions are run from it folder

### Generate data

Run the following command to generate a dataset: 

```
python3 generatorSentence.py --data='../datasets/data.csv'
```
Arguments:

**--data**, path to output data file in csv format;

**--num**, number of sentences to generate ***(optional)***.

### Train model

Run the following command to train your model on previously generated dataset:
```
python3 trainModel.py --roberta='../models/ruRoberta-large' --model='../models/model.pt' --data='../datasets/data.csv'
```
Arguments:

**--roberta**, path to Roberta model;

**--model**, path to trained model to saved it;

**--data**, path to data in csv format for training;

**--num**, number of data to train ***(optional)***;

**--epoch**, number of epochs to train ***(optional)***.

### Run trained model

Run the following command to execute model as question-answer style:
```
python3 runModel.py --roberta='../models/ruRoberta-large' --model='../models/model.pt'
```
Arguments:

**--roberta**, path to Roberta model;

**--model**, path to previously trained model;

**--metric**, path to test data in csv format to calculate metrics ***(optional)***;

## Authors

* **Kseniya Shutova** - *Created a dataset generator of motion commands* - [Renianida](https://github.com/Renianida)

* **Nikolay Andreychik** - *Created a neural network model to recognize motion commands* - [Koolana](https://github.com/Koolana)

See also the list of [contributors](https://github.com/Koolana/NLPForRobot/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [pytorch-seq2seq](https://github.com/bentrevett/pytorch-seq2seq) for excellent tutorials on seg2seg models 

## References

* [Abigail See and Manning, 2017] Abigail See, P. J. L. and Manning, C. D. (2017). Get to the point: Summarization with pointer-generator networks. 10:709.
* [Ashish Vaswani, 2017] Ashish Vaswani, Noam Shazeer, N. J. L. A. L. a. (2017). Attention is all you need. 31st Conference on Neural Information Processing Systems (NIPS 2017), Long Beach, CA, USA., 163(4):5998–6008.
* [Dzmitry Bahdanau, 2016] Dzmitry Bahdanau, KyungHyun Cho, K. C. (2016). Neural machine translation by jointly learning to align and translate. ICLR 2015.
* [Oriol Vinyals and Jaitly, 2015] Oriol Vinyals, M. F. and Jaitly, N. (2015). Pointer networks. in neural information processing systems.
* [Subendhu Rongali, 2020] Subendhu Rongali, Emilio Monti, L. S. W. H. (2020). Don’t parse, generate! a sequence to sequence architecture for task-oriented semantic parsing.

