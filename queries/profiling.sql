-- Анализ выполняемых запросов


-- Найдем ссылки на изображения в формате jpeg
with enclosures_messages as (
	select
		rm.id,
		rm.title,
		rm.enclosures_tuples :: text,
		cardinality(rm.enclosures_tuples) as enclosures_length
	from rss_messages rm
	where
		'Политика' = any(rm.categories_array)
		and rm.enclosures_tuples != '{}'
)
select
	em.id,
	(regexp_matches(em.enclosures_tuples, '(http[^,]*jpeg)', 'g'))[1]
from enclosures_messages em;


-- Посмотрим план выполнения запроса
explain with enclosures_messages as (
	select
		rm.id,
		rm.title,
		rm.enclosures_tuples :: text,
		cardinality(rm.enclosures_tuples) as enclosures_length
	from rss_messages rm
	where
		'Политика' = any(rm.categories_array)
		and rm.enclosures_tuples != '{}'
)
select
	em.id,
	(regexp_matches(em.enclosures_tuples, '(http[^,]*jpeg)', 'g'))[1]
from enclosures_messages em;


-- Посмотрим время выполнения запроса
explain analyze with enclosures_messages as (
	select
		rm.id,
		rm.title,
		rm.enclosures_tuples :: text,
		cardinality(rm.enclosures_tuples) as enclosures_length
	from rss_messages rm
	where
		'Политика' = any(rm.categories_array)
		and rm.enclosures_tuples != '{}'
)
select
	em.id,
	(regexp_matches(em.enclosures_tuples, '(http[^,]*jpeg)', 'g'))[1]
from enclosures_messages em;


-- Посмотрим подробно о выполнении запроса
explain analyze verbose with enclosures_messages as (
	select
		rm.id,
		rm.title,
		rm.enclosures_tuples :: text,
		cardinality(rm.enclosures_tuples) as enclosures_length
	from rss_messages rm
	where
		'Политика' = any(rm.categories_array)
		and rm.enclosures_tuples != '{}'
)
select
	em.id,
	(regexp_matches(em.enclosures_tuples, '(http[^,]*jpeg)', 'g'))[1]
from enclosures_messages em;