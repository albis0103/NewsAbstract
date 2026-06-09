import re
from pathlib import Path

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>自由系統資安週報</title>
</head>
<body style="margin:0; padding:0; background-color:#F5F5F5; font-family:'Microsoft JhengHei', 'PingFang TC', 'Helvetica Neue', Arial, sans-serif;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F5F5F5;">
  <tr>
    <td align="center" style="padding:0;">
      <table role="presentation" width="640" cellpadding="0" cellspacing="0" border="0" style="max-width:640px; width:100%;">

        <!-- ===== HEADER BANNER ===== -->
        <tr>
          <td style="background-color:#FFFFFF; padding:0;">
            <img src="https://static.newsleopard.com/40286b726bbff35c016bf986959b0796/2025-12-04-06-34-CRE81XAz"
                 alt="自由系統資安週報"
                 width="640"
                 style="display:block; width:100%; height:auto; border:0;">
          </td>
        </tr>
        <!-- ===== GREETING ===== -->
        <tr>
          <td style="background-color:#FFFFFF; padding:15px 24px 18px 24px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="color:#333333; font-size:14px; line-height:22px;">
                  <p style="margin:0 0 8px 0;">親愛的客戶您好</p>
                  <p style="margin:0;">自由系統資安服務團隊本週有以下情資分析供您參考：</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ===== SECTION HEADER: 本週重大資安事件 ===== -->
        <tr>
          <td style="background-color:#288BC4; padding:6px 24px;">
            <p style="margin:0; font-size:15px; font-weight:bold; color:#FFFFFF;">
              &#128276; 本週重大資安事件
            </p>
          </td>
        </tr>

        {events_html}

        <!-- ===== FOOTER TEXT ===== -->
        <tr>
          <td style="background-color:#FFFFFF; padding:18px 24px;" align="center">
            <p style="margin:0 0 4px 0; font-size:14px; color:#333333;">
              如果有其他問題，歡迎跟我們聯絡。謝謝。
            </p>
            <p style="margin:0; font-size:14px; color:#333333;">
              Cybersecurity Service Support
            </p>
          </td>
        </tr>

        <!-- ===== FOOTER BAR WITH SOCIAL ICONS ===== -->
        <tr>
          <td style="background-color:#288BC4; padding:12px 24px;" align="center">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="padding:0 12px;">
                  <a href="https://www.freedom.net.tw/">
                    <img src="https://static.newsleopard.com/nl/white/home.png"
                         alt="home" width="24" height="24"
                         style="display:inline-block; border:0;">
                  </a>
                </td>
                <td style="padding:0 12px;">
                  <a href="https://www.facebook.com/FreedomSystems/">
                    <img src="https://static.newsleopard.com/nl/white/facebook.png"
                         alt="facebook" width="24" height="24"
                         style="display:inline-block; border:0;">
                  </a>
                </td>
                <td style="padding:0 12px;">
                  <a href="https://www.linkedin.com/company/freedomsystems/">
                    <img src="https://static.newsleopard.com/nl/white/linkedin.png"
                         alt="linkedin" width="24" height="24"
                         style="display:inline-block; border:0;">
                  </a>
                </td>
                <td style="padding:0 12px;">
                  <a href="https://www.youtube.com/@FreedomSystems">
                    <img src="https://static.newsleopard.com/nl/white/youtube.png"
                         alt="youtube" width="24" height="24"
                         style="display:inline-block; border:0;">
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>

      </table>
      <!-- /Main container -->

    </td>
  </tr>
</table>

</body>
</html>'''

EVENT_TEPLATE = EVENT_TEMPLATE = """\
        <!-- ===== EVENT {n} ===== -->
        <tr>
          <td style="background-color:#FFFFFF; padding:18px 30px;">
            <p style="margin:24px 0 12px 0; font-size:14.5px; font-weight:bold; color:#333333;">
              {title}
            </p>
 
            <p style="margin:0 0 4px 0; font-size:14px; color:#025EB3;">
              <strong>&#128197; 發生時間 : </strong>
            </p>
            {date_html}
 
            <p style="margin:0 0 4px 0; font-size:14px; color:#025EB3;">
              <strong>&#127919; 影響範圍 :</strong>
            </p>
            {scope_html}
 
            <p style="margin:0 0 4px 0; font-size:14px; color:#333333;">
              ⚠️ <strong>潛在影響：</strong>
            </p>
            {impact_html}
 
            <p style="margin:0 0 4px 0; font-size:14px; color:#333333;">
              &#128221; <strong>重點整理 ：</strong>
            </p>
            {summary_html}
 
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:12px 0 0 0;">
              <tr>
                <td style="background-color:#1279C7; border-radius:4px; padding:8px 20px;">
                  <a href="{url}"
                     style="color:#FFFFFF; text-decoration:none; font-size:14px; font-weight:bold; letter-spacing:0.75px;">
                    了解更多
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>
"""

DIVIDER = '''        <tr>
          <td style="background-color:#FFFFFF; padding:0 24px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="border-top:1px solid #DDDDDD; font-size:0; line-height:0; height:1px;">&nbsp;</td>
              </tr>
            </table>
          </td>
        </tr>'''

#clean the prefix: '-' and space
def clean(text: str):
    lines = [l.strip() for l in text.strip().splitlines()]
    cleaned = []
    for line in lines:
        line = re.sub(r"^[-–]\s*", '', line)
        if line: cleaned.append(line)
    return cleaned

# dict: [field] -> field digest
FIELD_PATTERNS = {
    'title': r"1\.\s\[標題\][：:]?\s*\n(.*?)(?=\n\s*\n|\n\s*\d+\.)",
    'date': r"3\.\s\[發生時間\][：:]?\s*\n(.*?)(?=\n\s*\n\s*\d+\.|\n\s*\d+\.)",
    'scope': r"4\.\s\[影響範圍\][：:]?\s*\n(.*?)(?=\n\s*\n\s*\d+\.|\n\s*\d+\.)",
    'impact': r"5\.\s\[潛在影響\][：:]?\s*\n(.*?)(?=\n\s*\n\s*\d+\.|\n\s*\d+\.)",
    'summary': r"6\.\s\[重點整理\][：:]?\s*\n(.*?)(?=\n\s*\n\s*\d+\.|\n\s*\d+\.)",
    'url':r"7\.\s\[新聞網址\][：:]?\s*\n\s*(https?://\S+)",
}
def parse_event(raw: str) -> dict:
    result = {}
    for field, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, raw, flags=re.DOTALL)
        if match:
            result[field] = clean(match.group(1))
        else:
            result[field] = []
    if result['url']:
        result['url'] = result['url'][0] if isinstance(result['url'], list) else result['url']
    else:
        result['url'] = '#'
    return result

# transform list[str] -> <p>
def _lines_to_html(lines: list[str]) -> str:
    """將 list of str 轉為多個 <p> 段落。"""
    return "".join(
        f'<p style="margin:0 0 10px 0; font-size:11pt; line-height:20px; color:#000000;">{line}</p>'
        for line in lines
    )
def _meta_lines_to_html(lines: list[str], color: str = "#025EB3") -> str:
    return "".join(
        f'<p style="margin:0 0 4px 0; font-size:14px; line-height:20px; color:{color};">{line}</p>'
        for line in lines
    )

def render_event_block(n: int, event: dict) -> str:
    title = event["title"][0] if event["title"] else f"事件 {n}"

    date_html   = _meta_lines_to_html(event["date"])   or '<p style="margin:0 0 4px 0; font-size:14px; color:#025EB3;">—</p>'
    scope_html  = _meta_lines_to_html(event["scope"])  or '<p style="margin:0 0 4px 0; font-size:14px; color:#025EB3;">—</p>'
    impact_html = _lines_to_html(event["impact"])      or '<p style="margin:0 0 12px 0; font-size:11pt; color:#333333;">—</p>'
    summary_html= _lines_to_html(event["summary"])     or '<p style="margin:0 0 10px 0; font-size:11pt; color:#000000;">—</p>'
    return EVENT_TEMPLATE.format(
        n=n, 
        title = title,
        date_html = date_html,
        scope_html = scope_html,
        impact_html = impact_html,
        summary_html = summary_html,
        url = event['url'],
    )
def render_report(events: list[dict]) -> str:
    assert len(events) == 3

    blocks = []
    for i,event in enumerate(events, start = 1):
        blocks.append(render_event_block(i, event))
        if i<3:
            blocks.append(DIVIDER)
    events_html = '\n'.join(blocks)
    return HTML_TEMPLATE.format(
        events_html = events_html
    )

def main():
    base = Path('data')
    events = []
    for i in range(1,4):
        raw = (base/f"txt{i}.txt").read_text(encoding='utf-8')
        events.append(parse_event(raw=raw))
    html = render_report(events=events)
    Path('output.html').write_text(html, encoding='utf-8')
if __name__ == '__main__':
    main()