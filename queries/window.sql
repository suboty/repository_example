-- Оконные функции

-- Сгруппируем сообщения по хэшу источников (group by)
select count(*) from rss_messages rm
group by rm.source_hash;


-- Сгруппируем сообщения по хэшу источников (over)
select count(*) over (partition by rm.source_hash)
from rss_messages rm;


-- Посчитаем статистику по количеству ссылок (агрегирующие)
select
	"source",
	enclosures_length,
	sum(enclosures_length) over (partition by "source") as sum_enclosures_length,
	avg(enclosures_length) over (partition by "source") as avg_enclosures_length,
	count(enclosures_length) over (partition by "source") as count_enclosures_length,
	min(enclosures_length) over (partition by "source") as min_enclosures_length,
	max(enclosures_length) over (partition by "source") as max_enclosures_length
from messages_extra_2024_01_01
order by enclosures_length desc;


-- Посчитаем процент вклада каждого сообщения
-- в общее количество ссылок источника
-- в определенный день
select
	id,
	"source",
	enclosures_length,
	sum(enclosures_length) over (partition by "source"),
	round(
		(
			enclosures_length::float / sum(enclosures_length) over (partition by "source")::float
		) * 100
	)::text || '%' as percent_links
from messages_extra_2024_01_01
order by enclosures_length desc;


-- Посчитаем ранг для интервалов публикаций по источникам (ранжирующие)
select
	"source",
	publication_interval,
	row_number() over (partition by "source" order by publication_interval desc),
	rank() over (partition by "source" order by publication_interval desc),
	dense_rank() over (partition by "source" order by publication_interval desc)
from messages_extra_2024_08_16;


-- Выведем 10 "лучших" сообщений по количеству ссылок
with best_messages as (
	select
		"source",
		link,
		publication_interval,
		dense_rank() over (partition by "source" order by publication_interval desc) as "rank"
	from messages_extra_2024_08_16
)
select * from best_messages
where "rank" = 1
limit 10;