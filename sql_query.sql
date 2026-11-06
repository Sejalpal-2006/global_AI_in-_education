USE newschema;
SHOW TABLES;

SELECT * FROM `ai_education_usage_global_2015_2026 (2)`;

SELECT COUNT(*) AS total_rows
FROM `ai_education_usage_global_2015_2026 (2)`;

qeuery1: total records by countries and religions

SELECT country, region, year,
  COUNT(student_ai_usage_pct) AS total_records , COUNT(teacher_ai_usage_pct) as total_teacher_record
FROM `ai_education_usage_global_2015_2026 (2)` 
GROUP BY 
  country, 
  region,year;

query2: average student ai usage by country

Select country, avg(student_ai_usage_pct) as avg_student_ai_uasage
from `ai_education_usage_global_2015_2026 (2)`
group by country;

query3: average teacher ai usage by country

select country, avg(teacher_ai_usage_pct) as avg_teacher_ai_usage
from `ai_education_usage_global_2015_2026 (2)`
group by country;

 query4: Top 10 Countries by School AI Adoption
 
select country, avg(schools_ai_adoption_pct)
from `ai_education_usage_global_2015_2026 (2)`
group by country;

query5: Average daily AI usage by Region

select region,avg(avg_daily_ai_usage_min)
from `ai_education_usage_global_2015_2026 (2)`
group by region;

query6: Yearly AI Adoption Trend

select year, avg(student_ai_usage_pct)
from `ai_education_usage_global_2015_2026 (2)`
group by year;

query7: Monthly AI Usage Trend

select year,month,avg(student_ai_usage_pct)
from `ai_education_usage_global_2015_2026 (2)`
group by year,month

query8:AI Usage by Government Policy

select government_ai_policy,count(top_ai_tool) as total_ai_in_gov_policy
from `ai_education_usage_global_2015_2026 (2)`
group by government_ai_policy

query9:AI Usage by AI Curriculum

select ai_in_curriculum,count(top_ai_tool) as total_ai_use_in_curriculum
from `ai_education_usage_global_2015_2026 (2)`
group by ai_in_curriculum

query10:Urban-Rural Gap by Country

SELECT
    country,region,
    ROUND(AVG(urban_ai_usage_pct),2) AS Urban_AI_Usage,
    ROUND(AVG(rural_ai_usage_pct),2) AS Rural_AI_Usage,
    ROUND(AVG(urban_ai_usage_pct)-AVG(rural_ai_usage_pct),2) AS Usage_Gap
from `ai_education_usage_global_2015_2026 (2)`
GROUP BY country,region
ORDER BY Usage_Gap DESC;

query11: Countries with AI Usage above Global Average

select country, avg(student_ai_usage_pct)
from `ai_education_usage_global_2015_2026 (2)`
where student_ai_usage_pct > (select avg(student_ai_usage_pct) 
from `ai_education_usage_global_2015_2026 (2)`)
group by country

query12: Top 5 Countries in each Region

WITH CountryRank AS (
    SELECT
        region,
        country,
        ROUND(AVG(schools_ai_adoption_pct), 2) AS avg_ai_adoption,
        ROW_NUMBER() OVER (
            PARTITION BY region
            ORDER BY AVG(schools_ai_adoption_pct) DESC
        ) AS rn
    FROM `ai_education_usage_global_2015_2026 (2)`
    GROUP BY region, country
)
SELECT
    region,
    country,
    avg_ai_adoption
FROM CountryRank
WHERE rn <= 5
ORDER BY region, avg_ai_adoption DESC;



query14: Highest AI Adoption in each Year

select year,country,avg(schools_ai_adoption_pct)
FROM `ai_education_usage_global_2015_2026 (2)`
group by year,country;

query15: Year-over-Year Growth using lag()

with yearoveryear as(
  select year, round(avg(schools_ai_adoption_pct),2) as ai_adoption,
  round(LAG(avg(schools_ai_adoption_pct)) OVER (ORDER BY year),2) as previous_year_ai_adoptation
  FROM `ai_education_usage_global_2015_2026 (2)`
  GROUP BY year
)
select year,ai_adoption,previous_year_ai_adoptation,
round(ai_adoption- previous_year_ai_adoptation,2)as absolute_growth,
round(((ai_adoption - previous_year_ai_adoptation)
        / NULLIF(previous_year_ai_adoptation, 0)) * 100,
        2
    ) AS yoy_growth_pct
from yearoveryear
order by year;

query16:Rank Countries by Student AI Usage (DENSE_RANK())

select year,country, SUM(student_ai_usage_pct) as total_student_ai_uasage,
dense_rank() over(ORDER BY SUM(student_ai_usage_pct) ASC) as denserank
from `ai_education_usage_global_2015_2026 (2)`
group by year,country;

query17:Countries with Highest Gender Gap in AI Usage

select year,country,max(gender_gap_ai_usage_pct) as max_gender_gap,min(gender_gap_ai_usage_pct) min_gender_gap
from `ai_education_usage_global_2015_2026 (2)`
group by year,country;

query18: Countries with high Education Index but low School AI Adoption.  

WITH CountryStats AS (
    SELECT
        country,
        ROUND(AVG(education_index), 2) AS avg_education_index,
        ROUND(AVG(schools_ai_adoption_pct), 2) AS avg_school_ai_adoption
    FROM `ai_education_usage_global_2015_2026 (2)`
    GROUP BY country
),
Thresholds AS (
    SELECT
        AVG(avg_education_index) AS avg_education_index,
        AVG(avg_school_ai_adoption) AS avg_school_ai_adoption
    FROM CountryStats
)
SELECT
    c.country,
    c.avg_education_index,
    c.avg_school_ai_adoption
FROM CountryStats c
CROSS JOIN Thresholds t
WHERE c.avg_education_index > t.avg_education_index
  AND c.avg_school_ai_adoption < t.avg_school_ai_adoption
ORDER BY c.avg_education_index DESC;

query19: Countries above the global average Student AI Usage.

WITH GlobalAverage AS (
    SELECT
        AVG(student_ai_usage_pct) AS global_avg_student_usage
    FROM `ai_education_usage_global_2015_2026 (2)`
),
CountryUsage AS (
    SELECT
        country,
        ROUND(AVG(student_ai_usage_pct), 2) AS avg_student_ai_usage
    FROM `ai_education_usage_global_2015_2026 (2)`
    GROUP BY country
)
SELECT
    c.country,
    c.avg_student_ai_usage,
    ROUND(g.global_avg_student_usage, 2) AS global_average
FROM CountryUsage c
CROSS JOIN GlobalAverage g
WHERE c.avg_student_ai_usage > g.global_avg_student_usage
ORDER BY c.avg_student_ai_usage DESC;

query20:Count of Countries with AI Curriculum.

SELECT
    COUNT(DISTINCT country) AS countries_with_ai_curriculum
FROM `ai_education_usage_global_2015_2026 (2)`
WHERE ai_in_curriculum = 'Yes';