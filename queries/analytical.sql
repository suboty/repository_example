-- Аналитические запросы

-- Посмотрим таблицы
select * from rss_messages rm;
select * from sources s;


-- Посчитаем количество
select count(*) from rss_messages rm;
select count(*) from sources s;


-- Посмотрим сообщения в конкретный интервал дат
select * from rss_messages rm
where
	rm.public_time < '2024-02-25'
	and rm.public_time > '2024-01-25';


-- Посмотрим сообщения в конкретный интервал дат (через between)
select * from rss_messages rm
where
	rm.public_time between '2024-01-25' and '2024-02-25';


-- Посмотрим текст сообщений со словом США
select
	rm.description
from rss_messages rm
where
	rm.description like '%США%';


-- Посмотрим текст сообщений со словом США (нижний регистр)
select
	rm.description
from rss_messages rm
where
	rm.description ilike '%США%';


-- Посмотрим текст сообщений по некоторому паттерну
select
	title
from (
	select
		rm.title,
		substring(rm.title, 'США|Америка') as match_string
	from rss_messages rm)
where match_string is not null;


-- Помотрим сообщения где есть автор и отсортируем их времени публикации
select * from rss_messages rm
where rm.author is not null
order by rm.public_time desc;


-- Проверим предыдущий запрос
with sort_messages as (
	select * from rss_messages rm
	where rm.author is not null
	order by rm.public_time desc
)
select count(*) from sort_messages;


-- Исправим запрос с сортировкой
with sort_messages as (
	select * from rss_messages rm
	where rm.author != ''
	order by rm.public_time desc
)
select * from sort_messages;

-- Посмотрим сообщения с определенным тегом
select * from rss_messages rm
where 'Россия' = any(rm.tags_array);


-- Посмотрим сообщения с определенными тегами
select * from rss_messages rm
where rm.tags_array @> '{"Россия", "БРИКС"}';


-- Посмотрим связи сообщений по определенной категории
select
	rm.title,
	rm.enclosures_tuples :: text,
	cardinality(rm.enclosures_tuples) as enclosures_length
from rss_messages rm
where
	'Политика' = any(rm.categories_array)
	and rm.enclosures_tuples != '{}';


-- Отсортируем сообщения по количеству связей
with enclosures_messages as (
	select
		rm.title,
		rm.enclosures_tuples :: text,
		cardinality(rm.enclosures_tuples) as enclosures_length
	from rss_messages rm
	where
		'Политика' = any(rm.categories_array)
		and rm.enclosures_tuples != '{}'
)
select * from enclosures_messages em
order by em.enclosures_length desc;


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


-- Посмотрим сообщения, опубликованные день в день
select * from rss_messages rm
where date(rm.public_time) = date(rm.source_time);


-- Посчитаем статистику день в день
with day_by_day as (
	select count(*) from rss_messages rm
	where date(rm.public_time) = date(rm.source_time)
),
not_day_by_day as (
	select count(*) from rss_messages rm
	where date(rm.public_time) != date(rm.source_time)
)
select 'day by day' as "case", * from day_by_day
union all
select 'not day by day' as "case", * from not_day_by_day;


-- Посчитаем процент по интервалам сбора
with intervals as (
	select
		case
			when date(rm.public_time) = date(rm.source_time) then 'no distance'
			when date(rm.source_time) - date(rm.public_time) = 1 then 'one day'
			when date(rm.source_time) - date(rm.public_time) = 2 then 'two days'
			else 'more then two days'
		end as interval_case
	from rss_messages rm
)
select interval_case, count(*) from intervals
group by interval_case;


-- Посмотрим распределение по источникам (через group by)
select
	s.source_name,
	count(*) as messages_number
from rss_messages rm
join sources s on rm.source_hash = s.source_hash
group by s.source_name;


-- Посмотрим распределение по источникам (через with)
with messages_and_sources as (
	select *
	from rss_messages rm
	join sources s on rm.source_hash = s.source_hash
)
select
	mas.source_name,
	count(*) as messages_number
from messages_and_sources mas
group by mas.source_name;