[![Validate and Index BED file](https://github.com/DoeringLab/kn99_variants/actions/workflows/validate-bed.yml/badge.svg)](https://github.com/DoeringLab/kn99_variants/actions/workflows/validate-bed.yml)

# kn99_variants

This repository stores a bed file describing regions that should be excluded from
WGS samples which have KN99 as a parent strain. The bedfile can be used in nextflow
workflows by providing the following path:

https://raw.githubusercontent.com/DoeringLab/kn99_variants/main/kn99_exclude_regions.bed

## Updaing kn99_exclude_regions.bed

To update the bed file, you can click on the file, and then in the top right hand side, 
you'll see a pencil icon. Click the pencil icon and a new page will load where you 
can make edits.

### ***IMPORTANT***
We are using a [BED6 format file](https://en.wikipedia.org/wiki/BED_(file_format)), which
means that the first six columns specified in that link are present. BED files are tab 
separated and, critically, **0 indexed half open**.

This means to describe the first position on the chromosome, the bed entry would look like this:

```raw
CP022321.1	0	1	.	0	.
```

It can be very confusing because VCF files and the browser are 1-indexed, so the same position
in the browser, or in a VCF file, would have the coordinate `CP022321.1:1`.

That means that if you add an entry, and you are looking at a VCF file which has just the first
position, then you'll need to subtract 1 from that position. The end position would actually be
the value that is displayed in the VCF file. If you have questions, ask. The same goes for the
browser -- make sure you subtract 1 from the coordinates that appear in the browser.

The file is currently sorted, so please find, in the file, where your new addition should go. The
best way to add your new line is to copy the line above and paste it in, making edits as needed.

## Automatic Checks and Indexing

When you commit a change to `kn99_exclude_regions.bed` and push it to the main branch
(which will happen automatically when you hit "commit" if you are editing this through
github), there is an automatic workflow that is initiated. It will validate that the bed
file is still a correct bed file, and then it will run `GATK IndexFeatureFile` to re-create
the `kn99_exclude_regions.bed.idx` file. If your application requires the `.idx` file, then
you'll need to wait until the workflow completes, ~30 seconds, which you can watch if you 
click on the "actions" tab.  

If the workflow is successful, then the status badge will remain green:

[![Validate and Index BED file](https://github.com/DoeringLab/kn99_variants/actions/workflows/validate-bed.yml/badge.svg)](https://github.com/DoeringLab/kn99_variants/actions/workflows/validate-bed.yml)

if that badge is anything other than green (or if the workflow is currently running), then
you should not try to use the bed file or the .idx file -- it is possible that you messed up
the bed file format, or that the `GATK IndexFeatureFile` failed. If the badge is red, then 
please let a computationally inclined peer know.
