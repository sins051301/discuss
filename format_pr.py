#!/usr/bin/env python3
"""raw.json을 읽어 원문 그대로 보존한 Markdown 정리본을 생성합니다."""

import json
import sys
import os
import re
from datetime import datetime


def format_date(iso_str):
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso_str[:16]


def clean_body(body):
    if not body:
        return "*(내용 없음)*"
    return body.strip()


def format_pr_page(data):
    pr = data["pr"]
    meta = data["meta"]

    lines = []
    lines.append("---")
    lines.append(f'sidebar_label: "{meta["repo"]} PR #{meta["number"]}"')
    lines.append("sidebar_position: 1")
    lines.append("---")
    lines.append("")
    lines.append(f"# {pr['title']}")
    lines.append("")
    lines.append(f"> **원문 PR**: {meta['url']}")
    lines.append(f"> **저장소**: {meta['owner']}/{meta['repo']} | **작성자**: @{pr['user']['login']} | **상태**: {'merged' if pr['merged'] else pr['state']}")
    lines.append(f"> **생성일**: {format_date(pr['created_at'])[:10]} | **머지일**: {format_date(pr.get('merged_at', ''))[:10]}")
    lines.append(f"> **변경**: +{pr['additions']} / -{pr['deletions']} ({pr['changed_files']}개 파일)")
    if pr.get("labels"):
        labels = ", ".join(f"`{l}`" for l in pr["labels"])
        lines.append(f"> **라벨**: {labels}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # PR body
    if pr.get("body"):
        lines.append("## PR 설명 (원문)")
        lines.append("")
        lines.append(clean_body(pr["body"]))
        lines.append("")
        lines.append("---")
        lines.append("")

    # 일반 댓글
    comments = sorted(data["comments"], key=lambda c: c["created_at"])
    if comments:
        lines.append(f"## 토론 ({len(comments)}건)")
        lines.append("")

        for i, c in enumerate(comments, 1):
            date = format_date(c["created_at"])
            lines.append(f"### #{i} — @{c['user']} — {date}")
            lines.append("")
            lines.append(clean_body(c["body"]))
            lines.append("")
            lines.append("---")
            lines.append("")

    # 리뷰 코멘트 (코드 리뷰)
    review_comments = sorted(data["review_comments"], key=lambda c: c["created_at"])
    if review_comments:
        lines.append(f"## 코드 리뷰 코멘트 ({len(review_comments)}건)")
        lines.append("")

        for i, c in enumerate(review_comments, 1):
            date = format_date(c["created_at"])
            path = c.get("path", "")
            line_info = ""
            if c.get("line"):
                line_info = f" L{c['line']}"
            elif c.get("original_line"):
                line_info = f" L{c['original_line']}"

            lines.append(f"### RC#{i} — @{c['user']} — {date}")
            if path:
                lines.append(f"**파일**: `{path}`{line_info}")
            lines.append("")
            lines.append(clean_body(c["body"]))
            lines.append("")
            lines.append("---")
            lines.append("")

    # 리뷰
    reviews = [r for r in data["reviews"] if r.get("body")]
    if reviews:
        lines.append(f"## 리뷰 ({len(reviews)}건)")
        lines.append("")
        for r in reviews:
            date = format_date(r["submitted_at"])
            state_map = {
                "APPROVED": "APPROVED",
                "CHANGES_REQUESTED": "CHANGES REQUESTED",
                "COMMENTED": "COMMENTED",
                "DISMISSED": "DISMISSED",
            }
            state = state_map.get(r["state"], r["state"])
            lines.append(f"### @{r['user']} — {state} — {date}")
            lines.append("")
            lines.append(clean_body(r["body"]))
            lines.append("")
            lines.append("---")
            lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("사용법: python3 format_pr.py <raw.json 경로>")
        sys.exit(1)

    json_path = sys.argv[1]
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    md = format_pr_page(data)

    out_dir = os.path.dirname(json_path)
    out_path = os.path.join(out_dir, "full.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    total = len(data["comments"]) + len(data["review_comments"])
    print(f"완료! {total}건 포맷팅 → {out_path}")


if __name__ == "__main__":
    main()
