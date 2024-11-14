-- Представления


-- Добавим к таблице интервалы публикаций и источники
with intervals as (
	select
		rm.id,
		rm.link,
		s.source_name,
		s.site_url,
		rm.title,
		rm.public_time,
		rm.source_time,
		date(rm.source_time) - date(rm.public_time) as publication_interval
	from rss_messages rm
	join sources s on s.source_hash = rm.source_hash
)
select * from intervals;


-- Создадим представление с предыдущим запросом
create view messages as (
	with intervals as (
		select
			rm.id,
			rm.link,
			s.source_name,
			s.site_url,
			rm.title,
			rm.public_time,
			rm.source_time,
			date(rm.source_time) - date(rm.public_time) as publication_interval
		from rss_messages rm
		join sources s on s.source_hash = rm.source_hash
	)
	select * from intervals
);


-- Посмотрим созданное представление
select * from messages;


-- Немного изменим наше представление
create view messages_extra as (
	with intervals as (
		select
			rm.id,
			rm.link,
			s.source_name || ' | ' || s.site_url as "source",
			rm.title,
			rm.public_time,
			rm.source_time,
			date(rm.source_time) - date(rm.public_time) as publication_interval,
			cardinality(rm.enclosures_tuples) as enclosures_length
		from rss_messages rm
		join sources s on s.source_hash = rm.source_hash
	)
	select * from intervals
);


-- Посмотрим созданное представление
select * from messages_extra;


-- Создадим представление для выгрузки
create view messages_report as (
	with intervals as (
		select
			rm.id as "ID RSS сообщения",
			rm.link as "Ссылка на новость",
			s.source_name || ' | ' || s.site_url as "Источник",
			rm.title as "Заголовок новости",
			rm.public_time as "Дата публикации",
			rm.source_time as "Дата публикации в RSS ленте",
			date(rm.source_time) - date(rm.public_time) as "Разница в публикации в днях",
			cardinality(rm.enclosures_tuples) as "Количество связей с контентом"
		from rss_messages rm
		join sources s on s.source_hash = rm.source_hash
	)
	select * from intervals
);


-- Посмотрим созданное представление
select * from messages_report;