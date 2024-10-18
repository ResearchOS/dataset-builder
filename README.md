# dataset-builder
Build a Dataset, reading from a provided TOML file. Supported datasets are hierarchically structured data of any kind, with files split across folders. Each data file should represent one Data Object. Currently, multiple data objects per data file is not supported (see the [Roadmap](#roadmap))

This Dataset package supports any type of hierarchically structured data by specifying its metadata. It is the second tool developed for use with the ResearchOS platform (check out the first tool to generate DAG's of a data processing pipeline, [dagpiler](https://github.com/ResearchOS/dagpiler)).

## Roadmap
- Support datasets that have multiple data objects per file (i.e. one or more CSV files)