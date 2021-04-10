![CC0-1.0 License][license-shield] 
![Last commit][last-commit-shield]
![Language][language-shield]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <img src="images/logo.png" alt="Logo" width="80" height="80">
  <h3 align="center">Algorithmic trading learning repo</h3>

  <p align="center">
    This repo features code and tutorials for beginners to learn algo trading.
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About this repo](#-about-this-repo)
* [How to use](#-how-to-use)
* [Code overview](#-code-overview)
* [Development](#-development)
* [Contact](#-contact)
* [Acknowledgements](#-acknowledgements)
* [License](#%EF%B8%8F-license)

## 💻 About this repo 

This repo is built as part of the Final Year Project (FYP) at the Department of Computer Science of The University of Hong Kong (HKU). 

## 🤔 How to use

All the code could be found in the `/code` directory and the documentation could be accessed at [https://algo-trading.readthedocs.io/](https://algo-trading.readthedocs.io/).

(Note that the `/database` directory only contains example files. The actual database is stored in the HKU Department of Computer Science server.)  

## 📁 Code overview

### 1. Introduction
`intro-to-algotrading/`
* Basic data science
* Data scrapping


### 2. Technical Analysis
`technical-analysis_basics/`
* Chart analysis
* Trend analysis
* Basics of technical analysis

`technical-analysis_python/`
* Technical indicators implementation

`technical-analysis_julia/`
* Moving Average strategy implementation


### 3. Fundamental Analysis
`fundamental-analysis/`
* Ratio analysis & stock screening

`bankruptcy-prediction/`
* Prediction with machine learning models

### 4. Macroeconomic Analysis
`macroeconomic-analysis/`
* Property transaction data scrapping
* Property transaction data analysis
* Macroeconomic indicators analysis
* Property price prediction

### 5. Sentiment Analysis
`sentiment-analysis/`
* News data collection
* Tweets data collection
* VADER sentiment analysis
* Textblob sentiment analysis

### 6. Trade Execution
`paper-trading/`
* Paper Trading using Interactive Brokers (IB)

### 7. Integrated Strategies
`integrated-strategy/`
* Baseline model with data filters
* Trading signal generation with LSTM (single-feature)
* Trading signal generation with LSTM (multi-feature)
* Daily trading signal generation with LSTM + trade execution with IB


## 🔧 Development

The source code of the Sphinx documentation website could be found in the `/docs` directory. After updating any of the `*.rst` files in `/docs/source/`, run the following to generate the HTML files:

```
make html
```

## 📮 Contact

Project Link: https://awoo424.github.io/algotrading_fyp/

## 📚 Acknowledgements

* [Investopedia](https://www.investopedia.com/)
* [StockCharts](https://stockcharts.com/)
* [Technical Analysis Library in Python](https://github.com/bukosabino/ta) 

## ⚖️ License
Licensed under the Creative Commons Zero v1.0 Universal.
[Copy of the license](https://github.com/awoo424/algotrading/blob/master/LICENSE).

<!-- MARKDOWN LINKS & IMAGES -->
[license-shield]: https://img.shields.io/github/license/awoo424/algotrading
[last-commit-shield]: https://img.shields.io/github/last-commit/awoo424/algotrading?color=blue
[language-shield]: https://img.shields.io/github/languages/top/awoo424/algotrading?color=purple
