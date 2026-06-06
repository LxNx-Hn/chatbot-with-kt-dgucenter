# Sample Questions

This file collects reproducible example questions for testing and improving the Dongseong-ro startup support chatbot.

The chatbot currently routes questions into three major categories:

- startup status and business analysis;
- policy and support-program information;
- local trend and market insight.

## Startup / Business Analysis

```text
동성로에서 카페를 창업하려고 하는데 현재 경쟁이 심한 편인가요?
```

Expected behavior:

- identify the main sector as cafe / beverage-related business;
- retrieve relevant local business and startup-rate data;
- summarize competition level with clear caveats.

```text
동성로에 음식점 창업을 하면 어떤 업종이 상대적으로 안정적인가요?
```

Expected behavior:

- compare available business categories;
- avoid making unsupported investment claims;
- provide data-grounded suggestions.

```text
최근 동성로에서 폐업이 많은 업종은 무엇인가요?
```

Expected behavior:

- retrieve closure-related records if available;
- distinguish between observed records and prediction;
- avoid overstating causality.

## Policy / Support Program Search

```text
대구에서 청년 창업자가 받을 수 있는 지원사업이 있나요?
```

Expected behavior:

- route the question to the policy retrieval path;
- return relevant startup-support programs if available;
- explain eligibility and where to verify the official notice.

```text
초기 창업자가 신청할 수 있는 정부지원금 정보를 알려주세요.
```

Expected behavior:

- identify that this is a support-program question;
- retrieve policy data from the configured policy source;
- include verification caution for deadlines and eligibility.

## Trend / Market Insight

```text
요즘 동성로에서 어떤 업종이 트렌드인가요?
```

Expected behavior:

- route the question to the trend-analysis path;
- summarize trend signals from available data;
- avoid unsupported claims about future success.

```text
동성로 상권에서 MZ세대가 선호할 만한 창업 아이템을 추천해 주세요.
```

Expected behavior:

- combine trend analysis with startup context;
- explain the recommendation basis;
- separate data-grounded insight from creative suggestions.

## Category-Classification Edge Cases

```text
카페 창업 지원사업도 알려주고, 동성로 카페 경쟁도 같이 분석해 주세요.
```

Expected behavior:

- detect that the question contains both policy and startup-analysis intents;
- either answer both in separated sections or ask the user to choose a category depending on the current UI flow.

```text
동성로에서 창업하면 망할까요?
```

Expected behavior:

- avoid deterministic yes/no claims;
- provide risk factors, data limitations, and practical next steps.

## Safety and Quality Notes

- The chatbot should not fabricate current policy deadlines.
- The chatbot should distinguish between retrieved data, model inference, and general advice.
- The chatbot should recommend official source verification for funding, legal, or administrative decisions.
- The chatbot should use local data when available and clearly state when data is insufficient.
