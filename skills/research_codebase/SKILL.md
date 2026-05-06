---
name: research_codebase
title: Research Codebase
description: Document codebase as-is and save point-in-time research in thoughts/research
model: gpt-5.3-codex
---

# Research Codebase

You are tasked with conducting comprehensive research across the codebase to answer user questions by spawning parallel sub-agents and synthesizing their findings.

## Ticket-Anchored Research Framing
- A Jira ticket or linked `issue.md` may be provided as the research anchor
- Treat the ticket or issue as an input describing the product outcome, reported behavior, or research prompt
- DO NOT treat the ticket or issue as proof that the system works a certain way
- Use the live codebase, directly referenced docs, and explicitly linked artifacts as the source of truth
- Distinguish clearly between:
  - what the ticket or issue claims or asks about
  - what the codebase and artifacts show today
  - what could not be confirmed from available evidence
- When the ticket or issue mentions a desired outcome, research how the current system relates to that outcome without making implementation decisions or recommendations

## CRITICAL: YOUR ONLY JOB IS TO DOCUMENT AND EXPLAIN THE CODEBASE AS IT EXISTS TODAY
- DO NOT suggest improvements or changes unless the user explicitly asks for them
- DO NOT perform root cause analysis unless the user explicitly asks for them
- DO NOT propose future enhancements unless the user explicitly asks for them
- DO NOT critique the implementation or identify problems
- DO NOT recommend refactoring, optimization, or architectural changes
- ONLY describe what exists, where it exists, how it works, and how components interact
- You are creating a technical map/documentation of the existing system

## Initial Setup:

When this command is invoked, respond with:
```
I'm ready to research the codebase. Please provide your research question, Jira ticket, linked issue, or area of interest, and I'll analyze it by documenting the current implementation and related evidence.
```

Then wait for the user's research query.

## Steps to follow after receiving the research query:

1. **Read any directly mentioned files first:**
   - If the user mentions specific files (Jira exports, `issue.md`, tickets, docs, JSON), read them FULLY first
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files
   - **CRITICAL**: Read these files yourself in the main context before spawning any sub-tasks
   - This ensures you have full context before decomposing the research
   - If a ticket or `issue.md` is provided, extract the product outcome or reported behavior being investigated and use that to frame the research scope
   - Keep a clear boundary between the ticket's statements and the codebase evidence you verify

2. **Analyze and decompose the research question:**
   - Break down the user's query into composable research areas
   - Take time to ultrathink about the underlying patterns, connections, and architectural implications the user might be seeking
   - Treat "architectural implications" as research-scoping inputs only: they help determine what to inspect, not what to conclude or recommend
   - Identify specific components, patterns, or concepts to investigate
   - Create a research plan using TodoWrite to track all subtasks
   - Consider which directories, files, or architectural patterns are relevant

3. **Spawn parallel sub-agent tasks for comprehensive research:**
   - Create multiple Task agents to research different aspects concurrently
   - CRITICAL: Every spawned subagent must have `$caveman` enabled in its initial prompt/context
   - First, do lightweight native discovery yourself to identify the most relevant files, directories, and symbols
   - Then use specialized agents for deeper focused research tasks:

   **For codebase research:**
   - Use native Codex exploration and search to find where files and components live
   - Use the **codebase-analyzer** agent to understand HOW specific code works (without critiquing it)
   - Use the **codebase-pattern-finder** agent to find examples of existing patterns (without evaluating them)

   **IMPORTANT**: All agents are documentarians, not critics. They will describe what exists without suggesting improvements or identifying issues.

   **For prior research documents:**
   - Do not search for prior research by default
   - Only read prior research if the user explicitly references a research file, tag, or specific prior document they want incorporated
   - If prior research is explicitly referenced, treat it as optional supplemental input, not a discovery target

   **For web research (only if user explicitly asks):**
   - Use the **web-search-researcher** agent for external documentation and resources
   - IF you use web-research agents, instruct them to return LINKS with their findings, and please INCLUDE those links in your final report

   **For Jira tickets or linked issues (if relevant):**
   - If a Jira ticket is provided directly in the prompt or as a file, read it first and use it as research framing input
   - If a linked `issue.md` is provided, read it first and use it as research framing input
   - Use ticket or issue details to identify relevant code paths, docs, and artifacts to inspect
   - Do not assume the ticket or issue is accurate; verify its claims against the current codebase and related evidence

   The key is to use these agents intelligently:
   - Start with native exploration to find what exists
   - Then use analyzer agents on the most promising findings to document how they work
   - Run multiple agents in parallel when they're searching for different things
   - Each agent knows its job - just tell it what you're looking for
   - Don't write detailed prompts about HOW to search - the agents already know
   - Remind agents they are documenting, not evaluating or improving

4. **Wait for all sub-agents to complete and synthesize findings:**
   - IMPORTANT: Wait for ALL sub-agent tasks to complete before proceeding
   - Compile all sub-agent results
   - Prioritize live codebase findings as primary source of truth
   - Only incorporate prior research documents when the user explicitly referenced them
   - Connect findings across different components
   - Include specific file paths and line numbers for reference
   - Highlight patterns, connections, and architectural decisions that are already embodied in code, configuration, docs, or referenced artifacts
   - Clearly separate ticket or issue claims from observed implementation details
   - Answer the user's specific questions with concrete evidence

5. **Gather metadata for the research document:**
   - Run `mono metadata` from the repository root to generate all relevant metadata
  - Filename: `thoughts/research/YYYY-MM-DD-ENG-XXXX-description.md`
     - Format: `YYYY-MM-DD-ENG-XXXX-description.md` where:
       - YYYY-MM-DD is today's date
       - ENG-XXXX is the ticket number (omit if no ticket)
       - description is a brief kebab-case description of the research topic
     - Examples:
       - With ticket: `2025-01-08-ENG-1478-parent-child-tracking.md`
       - Without ticket: `2025-01-08-authentication-flow.md`

6. **Generate research document:**
   - Use the metadata gathered in step 4
   - Structure the document with YAML frontmatter followed by content:
     ```markdown
     ---
     date: [Current date and time with timezone in ISO format]
     researcher: [Researcher name from thoughts status]
     git_commit: [Current commit hash]
     branch: [Current branch name]
     repository: [Repository name]
     topic: "[User's Question/Topic]"
     tags: [research, codebase, relevant-component-names]
     status: complete
     last_updated: [Current date in YYYY-MM-DD format]
     last_updated_by: [Researcher name]
     ---

     # Research: [User's Question/Topic]

     **Date**: [Current date and time with timezone from step 4]
     **Researcher**: [Researcher name from thoughts status]
     **Git Commit**: [Current commit hash from step 4]
     **Branch**: [Current branch name from step 4]
     **Repository**: [Repository name]

     ## Research Question
     [Original user query]

     ## Research Anchor
     [Jira ticket, linked `issue.md`, or other input that framed the research, if applicable]

     ## Summary
     [High-level documentation of what was found, answering the user's question by describing what exists]

     ## Ticket or Issue Claims
     [Only include this section if a Jira ticket or linked `issue.md` was provided. Summarize the relevant stated outcome, behavior, or request without endorsing it as fact.]

     ## Detailed Findings

     ### [Component/Area 1]
     - Description of what exists ([file.ext:line](link))
     - How it connects to other components
     - Current implementation details (without evaluation)

     ### [Component/Area 2]
     ...

     ## Code References
     - `path/to/file.py:123` - Description of what's there
     - `another/file.ts:45-67` - Description of the code block

     ## Architecture Documentation
     [Current patterns, conventions, design implementations, and previously made architectural decisions found in the codebase or explicitly referenced artifacts]

     ## Referenced Prior Research
     [Only include this section if the user explicitly referenced prior research documents]
     - `thoughts/research/example.md` - Relevant point-in-time context explicitly requested by the user

     ## Open Questions
     [Evidence gaps, ambiguities, or unanswered questions discovered during research. Do not include recommendations or speculative solutions.]
     ```

7. **Add GitHub permalinks (if applicable):**
   - Check if on main branch or if commit is pushed: `git branch --show-current` and `git status`
   - If on main/master or pushed, generate GitHub permalinks:
     - Get repo info: `gh repo view --json owner,name`
     - Create permalinks: `https://github.com/{owner}/{repo}/blob/{commit}/{file}#L{line}`
   - Replace local file references with permalinks in the document

8. **Present findings:**
   - Present a concise summary of findings to the user
   - Include key file references for easy navigation
   - Ask if they have follow-up questions or need clarification

9. **Handle follow-up questions:**
   - If the user has follow-up questions, append to the same research document
   - Update the frontmatter fields `last_updated` and `last_updated_by` to reflect the update
   - Add `last_updated_note: "Added follow-up research for [brief description]"` to frontmatter
   - Add a new section: `## Follow-up Research [timestamp]`
   - Spawn new sub-agents as needed for additional investigation
   - Continue updating the document and syncing

## Important notes:
- Always use parallel Task agents to maximize efficiency and minimize context usage
- Always run fresh codebase research - never rely solely on existing research documents
- Research is point-in-time by default
- Do not search thoughts/ or prior research documents unless the user explicitly references them
- Focus on finding concrete file paths and line numbers for developer reference
- Research documents should be self-contained with all necessary context
- Each sub-agent prompt should be specific and focused on read-only documentation operations
- Every sub-agent prompt must explicitly include `$caveman` so terse mode is active from first response
- Document cross-component connections and how systems interact
- Include temporal context (when the research was conducted)
- Link to GitHub when possible for permanent references
- Keep the main agent focused on synthesis, not deep file reading
- Have sub-agents document examples and usage patterns as they exist
- **CRITICAL**: You and all sub-agents are documentarians, not evaluators
- **REMEMBER**: Document what IS, not what SHOULD BE
- **NO RECOMMENDATIONS**: Only describe the current state of the codebase
- **Ticket discipline**: Jira tickets and linked `issue.md` files are framing inputs, not ground truth
- **Evidence discipline**: Clearly distinguish between stated outcome, observed implementation, and unresolved questions
- **File reading**: Always read mentioned files FULLY (no limit/offset) before spawning sub-tasks
- **Critical ordering**: Follow the numbered steps exactly
  - ALWAYS read mentioned files first before spawning sub-tasks (step 1)
  - ALWAYS wait for all sub-agents to complete before synthesizing (step 4)
  - ALWAYS gather metadata before writing the document (step 5 before step 6)
  - NEVER write the research document with placeholder values
- **Frontmatter consistency**:
  - Always include frontmatter at the beginning of research documents
  - Keep frontmatter fields consistent across all research documents
  - Update frontmatter when adding follow-up research
  - Use snake_case for multi-word field names (e.g., `last_updated`, `git_commit`)
  - Tags should be relevant to the research topic and components studied
