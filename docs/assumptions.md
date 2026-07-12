# Assumptions & Limitations

## Assumptions

### Data Quality
- Daily prices accurately reflect market conditions
- No systematic errors in data collection
- Missing values are randomly distributed

### Event Analysis
- Events can be treated as discrete occurrences
- Event dates are approximately correct
- Major events have significant price impacts

### Statistical Modeling
- Price changes follow normal distribution (for change point model)
- Log returns are stationary
- Volatility is constant within regimes

## Limitations

### Correlation vs. Causation
Statistical correlation does not imply causation. While we identify associations between events and price changes, we cannot prove that events caused the changes.

### Data Frequency
- Daily data may miss intra-day events
- Weekend/holiday gaps affect analysis

### External Factors
- Model does not include GDP, inflation, or exchange rates
- Supply/demand fundamentals not directly modeled
- Market sentiment not captured

### Event Timing
- Exact event dates are approximate
- Events may have been anticipated by markets
- Multiple events can occur simultaneously

## Mitigation Strategies
- Use Bayesian inference for uncertainty quantification
- Provide confidence intervals for estimates
- Document all assumptions clearly
- Acknowledge limitations in final report