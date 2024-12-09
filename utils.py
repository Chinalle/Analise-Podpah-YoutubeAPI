import isodate
def format_youtube_duration(duration):
    # Converte a string ISO 8601 para um objeto timedelta
    parsed_duration = isodate.parse_duration(duration)
    
    # Calcula horas, minutos e segundos
    hours, remainder = divmod(parsed_duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f'{int(hours)}:{int(minutes)}:{int(seconds)}'