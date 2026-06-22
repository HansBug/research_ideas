# pairs_preview

## 示例 pair: sefm_ssc7_single_prompt_claude_sonnet35_0001

- 源文件：`assets/raw/llm_state_machine_modeling_4open.zip`
- 源定位：`nl_member=backend/resources/state_machine_descriptions.py; nl_symbol=SSC7_fall_2024; stm0_member=Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_f700645345f84b5acffd751f426344ed704910d9.txt`
- 源 ZIP SHA-256：`0e553383b5bd03702d29e5f68a3624fcc143a51da1fd0c9156b32ba51a5b61b4`
- NL hash：`a9803b9514ffe57d80c266a3c390298ca04e471d300c690045bb4479872ec1a8`
- STM_0 hash：`22aa85b151d2802084a41096bb9f3bec6a6d3c6c8d50e7c63626db2f0f66e8b4`
- eligibility：`final_pool_ready`
- caveat：ZIP 已 committed 且 locator 可回溯；公开学术 artifact 按引用原作处理。当前只证明 SSC7 有 generated STM_0，其余 8 个 NL 描述缺 generated text output，不能计为 generated pair。

### NL：SSC7 reactive-system description（节选）

```text
The Self-Service Checkout SSC7 is used by supermarkets to allow customers to scan their purchases and pay for them, often without any help of supermarket staff.
As shown in the figure on the right, the SSC7 consists of the following parts: (i) an area to the left to place items that still need to be scanned, (ii) a barcode reader, (iii) a touch screen, (iv) a scale in front of the touch screen to weigh items, (v) an area to the right with an integrated security scale where items are placed that have been scanned, (vi) a payment terminal to pay by credit card, (vii) a printer for the bill, and (viii) a light to indicate to a staff member that they are needed.
The SSC7 Software (SSC7S) interacts with parts (ii) to (viii). The barcode reader provides a scanned number to the SSC7S. The SSC7S uses the touch screen to show all information to the customer, and the customer presses buttons and provides the four-digit product code of items without barcode to the SSC7S. Both scales, the one in the front of the touch screen and the security scale, provide a weight to the SSC7S. The SSC7S sends a payment request to the payment terminal, which sends back a success message with an authorization
... [truncated; full text in pairs.jsonl and raw ZIP locator]
```

### STM_0：Claude Sonnet 3.5 single-prompt generated Umple

```text

class SSC7S {
  sm {
    Ready {
      scanBarcode [isValidBarcode] -> SecurityCheck;
      scanBarcode [!isValidBarcode] -> /{showError();} Ready;
      enterCode [isValidCode] -> WeighingItem;
      enterCode [!isValidCode] -> /{showError();} Ready;
      weighBag -> WeighingBag;
      pay [hasItems] -> Payment;
      timeout -> Timeout;
    }

    WeighingItem {
      weightReceived -> SecurityCheck;
      cancel -> Ready;
      requestCancel -> Override;
    }

    WeighingBag {
      weightReceived -> /{updateBagCount();} Ready;
      cancel -> Ready;
    }

    SecurityCheck {
      weightMatch -> Ready;
      weightMismatch -> Override;
      requestCancel -> Override;
    }

    Payment {
      success -> /{printBill();} Ready;
      failure -> /{showError();} Ready;
      cancel -> Ready;
    }

    Override {
      entry /{turnLightOn();}
      enterCode [isValidStaffCode] -> /{turnLightOff();} Ready;
      enterCode [!isValidStaffCode] -> /{showError();} Override;
    }

    Timeout {
      continue -> Ready;
      after(60) -> /{clearAll();} Ready;
    }
  }
}


```
