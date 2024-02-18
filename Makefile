BASELINES = "max-entropy" "synthetic-data-iql"
RESULTS_TWO_SAMPLE_TESTING = results/two-sample-testing/
RESULTS_DISTANCE_METRICS = results/distance-metrics/

.PHONY: two_sample
two_sample:
	mkdir -p $(RESULTS_TWO_SAMPLE_TESTING)
	@for syn_data_source in $(BASELINES); do \
		python scripts/two_sample_testing.py --training test-data/real/ignored.csv --compare test-data/synthetic/$$syn_data_source.csv > $(RESULTS_TWO_SAMPLE_TESTING)/$$syn_data_source.csv; \
	done

.PHONY: distance
distance:
	mkdir -p $(RESULTS_DISTANCE_METRICS)
	@for syn_data_source in $(BASELINES); do \
		python scripts/assess_fit.py --training test-data/real/ignored.csv --compare test-data/synthetic/$$syn_data_source.csv > $(RESULTS_DISTANCE_METRICS)/$$syn_data_source.csv; \
	done
	python scripts/assess_fit.py --training test-data/real/ignored.csv --compare test-data/real/test.csv > $(RESULTS_DISTANCE_METRICS)/held-out-data.csv; \
