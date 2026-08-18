# Download FigShare Datasets

This helps you download datasets from FigShare. You can use this script to download datasets using their FigShare IDs.

The current script only gives you the curl command to download the dataset. You can copy and paste the command into your terminal to download the dataset.

## Setup

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Example 1

```bash
python get_download_links.py "https://figshare.com/ndownloader/articles/27261219?private_link=ee85bb1880921326249b"
```

## Example 2

```bash
python get_download_links.py "https://plus.figshare.com/articles/dataset/Processed_data_for_X-Atlas_Orion_Genome-wide_Perturb-seq_Datasets_via_a_Scalable_Fix-Cryopreserve_Platform_for_Training_Dose-Dependent_Biological_Foundation_Models/29190726"
```
