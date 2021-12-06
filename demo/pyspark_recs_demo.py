# PySpark Demo based on PS3 Q2
#
# We will use PySpark and SQL to estimate the average number of heating
# and cooling degree days (base temperature 65 °F) for residences in each
# Census region using the 2009 RECS data.
#
# Date: December 6, 2021
# Author: James Henderson
# 79: -------------------------------------------------------------------------

# imports: --------------------------------------------------------------------
import pandas as pd
import subprocess

# read data and register in SQL: ----------------------------------------------
path = '/user/jbhender/stats507/demo/'
stems = ['recs09', 'w09']
tables = ['recs09', 'w09']

# dictionary of spark data frames
dfd = dict()
for stem, table in zip(stems, tables):
    # transfer to parquet
    pq_file = path + stem + '.parquet'
    
    # check if parquet file exists
    proc = subprocess.Popen(['hadoop', 'fs', '-test', '-e', pq_file])
    _ = proc.communicate()

    if proc.returncode == 0:
        # read existing parquet file
        dfd[stem] = sqlContext.read.parquet(pq_file)
    else:
        # read from feather and create parquet
        file_name = path + stem + '.csv'
        dfd[stem] = sqlContext.read.csv(
            file_name,
            header=True,
            inferSchema=True
        )
        dfd[stem].write.parquet(pq_file)

    # create a table handle
    dfd[stem].registerTempTable(table)

# compute point estimates: ----------------------------------------------------

pe_query = """
SELECT 
  region,
  sum(hdd65 * weight) / sum(weight) AS hdd65_avg,
  sum(cdd65 * weight) / sum(weight) AS cdd65_avg    
FROM recs09
GROUP BY region
"""

pe = sqlContext.sql(pe_query)
pe.registerTempTable('pe')
#pe.collect()

# compute replicate estimates: ------------------------------------------------

re_query = """
SELECT
  a.region,
  b.repl, 
  sum(a.hdd65 * b.rw) / sum(b.rw) as hdd65r,
  sum(a.cdd65 * b.rw) / sum(b.rw) as cdd65r
FROM recs09 a 
LEFT JOIN w09 b 
  ON b.id = a.id
GROUP BY region, repl
"""

re = sqlContext.sql(re_query)
re.registerTempTable('re')

# compute variance: -----------------------------------------------------------

se_query = """
SELECT
  pe.region,
  2 * sqrt(avg((hdd65_avg - hdd65r) * (hdd65_avg - hdd65r))) as hdd_se,
  2 * sqrt(avg((cdd65_avg - cdd65r) * (cdd65_avg - cdd65r))) as cdd_se 
FROM re
INNER JOIN pe 
  ON re.region = pe.region
GROUP BY pe.region
"""

se = sqlContext.sql(se_query)
se.registerTempTable('se')

# compute upper and lower bounds: ---------------------------------------------

ci_query = """
SELECT 
  pe.region, 
  hdd65_avg,
  hdd65_avg - 1.96 * hdd_se AS hdd65_lwr,
  hdd65_avg + 1.96 * hdd_se AS hdd65_upr,
  cdd65_avg,
  cdd65_avg - 1.96 * cdd_se AS cdd65_lwr,
  cdd65_avg + 1.96 * cdd_se AS cdd65_upr
FROM pe
INNER JOIN se
  ON pe.region = se.region
"""

ci = sqlContext.sql(ci_query)
ci = ci.persist()
ci_df = ci.collect()

# write result to disk: -------------------------------------------------------
ci.coalesce(1).write.csv(path + 'avg_hdd_cdd_2009.csv', header=True)

# 79: -------------------------------------------------------------------------
