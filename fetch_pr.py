#!/usr/bin/env python3
"""GitHub PR 토론 크롤러 - gh CLI를 사용하여 PR의 모든 토론 데이터를 수집합니다."""

import subprocess
import json
import sys
import re
import os
from datetime import datetime
from typing import Dict, List, Tuple, Union


def parse_pr_url(url: str) -> Tuple[str, str, int]:
    """PR URL에서 owner, repo, pull_number를 추출"""
    pattern = r"github\.com/([^/]+)/([^/]+)/pull/(\d+)"
    match = re.search(pattern, url)
    if not match:
        print(f"[오류] 유효하지 않은 PR URL: {url}")
        print("형식: https://github.com/owner/repo/pull/123")
        sys.exit(1)
    return match.group(1), match.group(2), int(match.group(3))


def gh_api(endpoint: str) -> Union[Dict, List]:
    """gh api 단일 호출"""
    result = subprocess.run(
        ["gh", "api", endpoint, "-H", "Accept: application/vnd.github.v3+json"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[오류] gh api 호출 실패: {endpoint}")
        print(result.stderr)
        return {}
    return json.loads(result.stdout)


def gh_api_paginate(endpoint: str) -> List:
    """gh api 페이지네이션 처리 - 모든 결과를 가져올 때까지 반복"""
    all_data = []
    page = 1
    while True:
        separator = "&" if "?" in endpoint else "?"
        url = f"{endpoint}{separator}per_page=100&page={page}"
        result = subprocess.run(
            ["gh", "api", url, "-H", "Accept: application/vnd.github.v3+json"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"[경고] 페이지 {page} 호출 실패: {url}")
            break
        data = json.loads(result.stdout)
        if not data or not isinstance(data, list):
            break
        all_data.extend(data)
        print(f"  - 페이지 {page}: {len(data)}건 수집")
        if len(data) < 100:
            break
        page += 1
    return all_data


def fetch_pr(owner: str, repo: str, number: int) -> Dict:
    """PR의 모든 토론 데이터를 수집"""
    base = f"/repos/{owner}/{repo}"

    print(f"\n{'='*60}")
    print(f"  PR 크롤링: {owner}/{repo}#{number}")
    print(f"{'='*60}\n")

    # 1) PR 메타데이터
    print("[1/4] PR 메타데이터 수집...")
    pr_data = gh_api(f"{base}/pulls/{number}")

    # 2) 일반 댓글 (이슈 API 사용 - PR 전체에 대한 토론)
    print("[2/4] 일반 토론 댓글 수집...")
    comments = gh_api_paginate(f"{base}/issues/{number}/comments")
    print(f"  => 총 {len(comments)}건\n")

    # 3) 코드 리뷰 댓글 (코드 라인별 리뷰)
    print("[3/4] 코드 리뷰 댓글 수집...")
    review_comments = gh_api_paginate(f"{base}/pulls/{number}/comments")
    print(f"  => 총 {len(review_comments)}건\n")

    # 4) 리뷰 (Approve, Request Changes 등)
    print("[4/4] 리뷰 수집...")
    reviews = gh_api_paginate(f"{base}/pulls/{number}/reviews")
    print(f"  => 총 {len(reviews)}건\n")

    return {
        "meta": {
            "owner": owner,
            "repo": repo,
            "number": number,
            "url": f"https://github.com/{owner}/{repo}/pull/{number}",
            "crawled_at": datetime.now().isoformat(),
        },
        "pr": {
            "title": pr_data.get("title", ""),
            "body": pr_data.get("body", ""),
            "state": pr_data.get("state", ""),
            "merged": pr_data.get("merged", False),
            "created_at": pr_data.get("created_at", ""),
            "updated_at": pr_data.get("updated_at", ""),
            "merged_at": pr_data.get("merged_at", ""),
            "closed_at": pr_data.get("closed_at", ""),
            "user": {
                "login": pr_data.get("user", {}).get("login", ""),
                "avatar_url": pr_data.get("user", {}).get("avatar_url", ""),
            },
            "labels": [l.get("name", "") for l in pr_data.get("labels", [])],
            "base": pr_data.get("base", {}).get("ref", ""),
            "head": pr_data.get("head", {}).get("ref", ""),
            "additions": pr_data.get("additions", 0),
            "deletions": pr_data.get("deletions", 0),
            "changed_files": pr_data.get("changed_files", 0),
        },
        "comments": [
            {
                "id": c.get("id"),
                "user": c.get("user", {}).get("login", ""),
                "avatar_url": c.get("user", {}).get("avatar_url", ""),
                "body": c.get("body", ""),
                "created_at": c.get("created_at", ""),
                "updated_at": c.get("updated_at", ""),
                "reactions": {
                    k: c.get("reactions", {}).get(k, 0)
                    for k in ["+1", "-1", "laugh", "hooray", "confused", "heart", "rocket", "eyes"]
                    if c.get("reactions", {}).get(k, 0) > 0
                },
            }
            for c in comments
        ],
        "review_comments": [
            {
                "id": c.get("id"),
                "pull_request_review_id": c.get("pull_request_review_id"),
                "in_reply_to_id": c.get("in_reply_to_id"),
                "user": c.get("user", {}).get("login", ""),
                "avatar_url": c.get("user", {}).get("avatar_url", ""),
                "body": c.get("body", ""),
                "path": c.get("path", ""),
                "line": c.get("line"),
                "original_line": c.get("original_line"),
                "start_line": c.get("start_line"),
                "diff_hunk": c.get("diff_hunk", ""),
                "created_at": c.get("created_at", ""),
                "updated_at": c.get("updated_at", ""),
            }
            for c in review_comments
        ],
        "reviews": [
            {
                "id": r.get("id"),
                "user": r.get("user", {}).get("login", ""),
                "avatar_url": r.get("user", {}).get("avatar_url", ""),
                "state": r.get("state", ""),
                "body": r.get("body", ""),
                "submitted_at": r.get("submitted_at", ""),
            }
            for r in reviews
        ],
    }


def main():
    if len(sys.argv) < 2:
        print("사용법: python3 fetch_pr.py <PR_URL>")
        print("예시:   python3 fetch_pr.py https://github.com/facebook/react/pull/31715")
        sys.exit(1)

    url = sys.argv[1]
    owner, repo, number = parse_pr_url(url)

    data = fetch_pr(owner, repo, number)

    # 출력 디렉토리 생성
    out_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "site", "docs", f"{repo}-pr-{number}"
    )
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, "raw.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    total = len(data["comments"]) + len(data["review_comments"]) + len(data["reviews"])
    print(f"{'='*60}")
    print(f"  완료! 총 {total}건의 토론 데이터 수집")
    print(f"  저장: {out_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
