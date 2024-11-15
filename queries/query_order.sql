-- Порядок выполнения select запроса


-- Первым всегда выполняется оператор FROM
select * from rss_messages rm;


-- Следующий этап - все JOIN-ы
select * from rss_messages rm
join sources s on s.source_hash = rm.source_hash;


-- Следующий этап - WHERE
select * from rss_messages rm
join sources s on s.source_hash = rm.source_hash
where date(rm.public_time) > '2024-01-01';


-- Далее группировка - GROUP BY
select s.source_name, count(*) from rss_messages rm
join sources s on s.source_hash = rm.source_hash
where date(rm.public_time) > '2024-01-01'
group by s.source_name, cardinality(rm.enclosures_tuples);


-- После группировки идет фильтрация групп - HAVING
select s.source_name, cardinality(rm.enclosures_tuples), count(*) from rss_messages rm
join sources s on s.source_hash = rm.source_hash
where date(rm.public_time) > '2024-01-01'
group by s.source_name, cardinality(rm.enclosures_tuples)
having cardinality(rm.enclosures_tuples) > 1;


-- Далее можно отсортировать - ORDER BY
select s.source_name, cardinality(rm.enclosures_tuples), count(*) from rss_messages rm
join sources s on s.source_hash = rm.source_hash
where date(rm.public_time) > '2024-01-01'
group by s.source_name, cardinality(rm.enclosures_tuples)
having cardinality(rm.enclosures_tuples) > 1
order by cardinality(rm.enclosures_tuples) desc;


-- Последним этапом идут ограничения - LIMIT
select s.source_name, cardinality(rm.enclosures_tuples), count(*) from rss_messages rm
join sources s on s.source_hash = rm.source_hash
where date(rm.public_time) > '2024-01-01'
group by s.source_name, cardinality(rm.enclosures_tuples)
having cardinality(rm.enclosures_tuples) > 1
order by cardinality(rm.enclosures_tuples) desc
limit 15;