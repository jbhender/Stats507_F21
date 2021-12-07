---
jupyter:
  jupytext:
    cell_metadata_json: true
    notebook_metadata_filter: rise
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  rise:
    autolaunch: true
    enable_chalkboard: true
    header: <a href="#/slide-0-0"> <h3> Stats 507 - PySpark </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## PySpark 
*Stats 507, Fall 2021*

James Henderson, PhD  
December 7, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
 - [Hadoop](#/slide-2-0)
 - [MapReduce](#/slide-3-0)
 - [HDFS](#/slide-4-0)
 - [PySpark](#/slide-5-0)
 - [RDD](#/slide-6-0)
 - [DataFrame](#/slide-7-0)
 - [SQL](#/slide-8-0)
 - [Takeaways](#/slide-9-0)
<!-- #endregion -->


<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Hadoop
> Apache Hadoop is a collection of open-source software utilities that 
> facilitates using a network of many computers to solve problems involving
> massive amounts of data and computation. It provides a software framework 
> for distributed storage and processing of big data using the MapReduce 
> programming model. Hadoop was originally designed for computer clusters built
> from commodity hardware, which is still the common use.
>  <cite>--[Wikipedia][hadoop] </cite>

[hadoop]: https://en.wikipedia.org/wiki/Apache_Hadoop
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Hadoop
 - Software library for *distributed* computing.
 - Designed to work with consumer-level computers connected over a network.
 - Intended to be resilient to failures of some cluster components.  
 - Accomplished through data-replication.
 - Implements MapReduce paradigm.   
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Hadoop Ecosystem
 - Map Reduce - framework for distributed computing
 - HDFS - Hadoop Distributed File System
 - PySpark - Spark's interactive Python Console. 
 - Yarn - job manager
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## MapReduce
 - [MapReduce][mr] is a programming paradigm for working with "massive"
   data distributed across a Hadoop cluster.
 - This distributed processing allows programs to flexibly scale to data 
   measured in petabytes (1 million GB or 1 thousand TB).  
 
 [mr]: https://www.ibm.com/topics/mapreduce
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## MapReduce
 - A MapReduce program consists of a *map* step and a *reduce* step:
    + The *map* steps work on chunks of data in parallel and return
      key-value pairs.
    + The *reduce* step aggregates those pairs into the desired outcome.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## HDFS
- The *Hadoop distributed file system* is a core part of the Hadoop framework.
- Splits files into large blocks and distributes them across nodes in a 
  cluster.
- Often used with replication.  Common to use 128 MB blocks with 3x replication.
- This is a nice introduction to HDFS using Legos:
  https://youtu.be/4Gfl0WuONMY  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## HDFS
 - The *distributed file system* is different from the POSIx home directory
   mounted to the login nodes used to access the hadoop cluster. 
 - Use linux-like file system commands after `hdfs dfs` to work with files.
 - Use `hdfs dfs -put <local_file> <path/new_file>` to put data into HDFS.  
 - Use `hdfs dfs -get <hdfs_file> <local_file>` to get data from HDFS.  
<!-- #endregion -->

```bash
ssh cavium-thunderx.arc-ts.umich.edu
hdfs dfs -ls stats507
hdfs dfs -ls /user/jbhender/stats507
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## HDFS-FUSE
 - Navigate to directory `/hadoop-fuse/user/<email>/` and use linux file system
   commands without `hdfs dfs` prefix. 

```bash
cd /hadoop-fuse/
ls /user/jbhender/stats507/
head -5 /user/jbhender/stats507/rectangles.csv
```
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## PySpark
 - PySpark is an interactive Python console for Spark.
 - Start a PySpark session as shown below.
 - Only `--master yarn` is necessary. 
<!-- #endregion -->

 ```bash
 pyspark --master yarn --queue default --num-executors=8 --executor-memory=1g
 ```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Existing Objects
 - When you launch PySpark, the following instances will be present:
    + `spark` - an instance of a `SparkSession()`,
    + `sc` - an instance of a `SparkContext()`,
    + `sqlContext` - an instance of `SQLContext()`. 
<!-- #endregion -->


<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Batch Mode
 - To run in batch mode, use `spark-submit`.
 - For SQL, add: `--conf spark.hadoop.metastore.catalog.default=hive`
 - Add the lines below to get to the same starting point as the interactive 
   shell. 
 - Taken from [here][cao].

 [cao]: https://github.com/caocscar/workshops/blob/master/pyspark/pyspark.md
<!-- #endregion -->

```python
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

conf = SparkConf()
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
```
<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## RDD
 - Spark stores data in a *Resilient Distributed Dataset* or [RDD][rdd].
 - An RDD is immutable, transformations result in a new RDD.
 - Resiliency is accomplished through data redundancy or *partitions* which
   also enables parallelism.

 [rdd]: https://spark.apache.org/docs/2.2.1/rdd-programming-guide.html#overview
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## RDD
 - Use `sc.parallelize()` to distribute the data.
 - Use `.repartition()` or `.coalesce()` to redistribute an existing RDD.
 - RDDs support two types of operation *transformations* and *actions*. 
 - We mostly won't use RDDs directly, instead using higher level SQL/DataFrame 
   instances.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## DataFrame
 - In [Spark][df], a "DataFrame is a *Dataset* organize into named columns." 
 - DataFrame instances support distributed processing.
 - Convert from a pandas DataFrame using `createDataFrame()`.
 - See more [here][qsdf].

 [df]: https://spark.apache.org/docs/latest/sql-programming-guide.html
 [qsdf]: https://spark.apache.org/docs/latest/api/python/getting_started/quickstart_df.html
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## SQL
 - DataFrames can be registered as SQL tables using the 
   `sqlContext.registerDataFrameAsTable()` method.
 - (Better) use the DataFrame's `.registerTempTable()` method so table's 
   don't persis across jobs. 
 - Run SQL queries against registered tables using `sqlContext.sql()`. 
 - For all but very simple queries, best to create a string instance 
   for the query. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## SQL/DataFrame Results
 - Use `.show()` to print a DataFrame (e.g. resulting from a SQL query).
 - Use `.collect()` to gather the results into memory.
 - By default, PySpark uses *lazy evaluation* -- results are formed only as 
   needed.
 - Use `.persist()` to save results so they don't need to be recomputed. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## SQL
  - *Structure Query Language* or SQL is a standard syntax for expressing
    data frame ("table") operations.
  - SQL is an *imperative* syntax - you specify what the result should look 
    like, rather than *declaring how* to achieve it.
  - SQL is a common way to interact with RDDs and DataFrames in PySpark. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Canonical Order
 - SQL statements appear using clauses in the canonical order below.
 - Not all clauses are present in all statement.
 - Often use LEFT/INNER/FULL OUTER `JOIN`s after `FROM`/`WHERE`.
<!-- #endregion -->

```sql
SELECT
FROM
WHERE
GROUP BY
HAVING
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## SQL Syntax
 - Identify the source table in `FROM`.
 - Use `WHERE` to specify a subset of data to include using conditions on \
   *existing tables* (in `FROM`)
 - Choose, transform, and rename columns using `SELECT`.
 - Use [aggregation functions][af] and `GROUP BY` for split-apply-combined 
   operations.

[rf]: https://spark.apache.org/docs/latest/sql-ref-functions-builtin.html#aggregate-functions
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Aliases
- After `FROM` use a short name to alias a table.
- Especially useful when table name needs a prefix with joins. 
- In `SELECT` rename a column/computations using `as`. 
- Create a table from a query by aliasing the statement with `AS`:

```sql
CREATE TABLE <name> AS SELECT ...
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Anonymous Tables
 - For complex queries, often helpful to express an intermediate results using
   an *anonymous* table `(SELECT ...) a`. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## JOINS
 - Work with data from multiple table by creating a *join* (a temporary merge).
 - Specify the keys to merge on using `ON` e.g. `ON a.id = b.id`.
 - Prefer `LEFT JOIN` or `INNER JOIN` for consistency. 
<!-- #endregion -->


<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
 - (Py)Spark enables parallel computations on massive datasets through
    distributed computing and data parallelism.
 - Resiliency is achieved through redundancy. 
 - Not generally the best choice for data that fits in memory. 
 - Basic SQL is essential knowledge beyond Spark.
<!-- #endregion -->
