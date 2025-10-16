
async def collect_reports(link_by_ads_ids: list):
    reports = []
    for link in link_by_ads_ids:
        # важно если в рекламе за указанную дату не было метрик результат None
        if link:
            report = await ozon_service.get_report(link)
            if report is not None:
                reports.extend(report)
    return reports