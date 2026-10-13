# Production lessons from actual work

These are reusable lessons from still-board and source-video production, not claims that a particular model always behaves this way. Preserve the user's actual medium, scope, and reference choices.

## References, sheets, and approval

**Read the image, not its name.** A sheet can contain an unsuitable angle, the wrong wardrobe state, an embedded label, or an actor name that doesn't match the pictured selected character. Inspect the panels and use the human's chosen appearance. Re-resolve references after board transfers/duplication.

**Keep source provenance clear.** Real/source references, generated sheets, finished frames, and rejected alternatives have different roles. If Preview-native generation is requested, don't silently substitute an externally generated draft as a source or represent an imported image as a native Preview take. External look-development drafts remain drafts unless selected.

**Don't generate redundant sheets.** Equipment already embedded in a chosen character sheet may need no separate prop sheet. A crowd reference isn't necessary for every background extra. Meaningful costume/action states can be variations; additional angles of the same state belong to that state's image set.

**Character-sheet layout is a choice.** A large full-body figure at left and sectioned angles/details at right worked well for human review. The exact built-in Character Creation preset is a different operation. Don't claim a hand-prompted sheet invoked that preset. Avoid background/location spill into identity references.

**Locations need actual spatial continuity.** Multi-angle sheets should describe one physical set, with consistent doors, road directions, furniture, vehicle entry, and lighting. A polished montage of incompatible environments is not a usable location reference. Isolated objects and environment-only sources reduce unwanted background/people transfer.

**Provisional anchors stay provisional.** A corrected anchor remains in review until accepted under the configured policy. It may serve as a bounded provisional input when explicitly authorized, with its role/state recorded and kept out of the approved library baseline. See [Change and approval checks](change-and-approval-checks.md).

## Anchors and camera direction

**Lock geography before covering it.** Generating independent camera views before establishing doors, rooms, furniture and positions causes continuity drift. Create representative anchors from the requested shot coverage; inspect cast, geography, object count, and state before dependents. Don't invent extra shots solely to populate an anchor registry.

**Reference roles must be explicit.** A blockout supplies camera, lens, horizon, and positions; the final prompt still needs natural weight shifts, gestures, and asymmetric human activity. A location sheet supplies geography, not all its panel cameras at once. A character sheet supplies appearance, not its rulers, captions, white background, or duplicate people.

**An opening frame is one instant.** Don't put every later action into the still prompt. If participants join during the shot, identify who is visible at its opening. Keep dialogue, shot duration, camera movement, and later action in the shot card/record. Extra action beats or inserts deserve their own identity rather than being mislabeled revisions.

**Camera variety follows storytelling.** Mix scale, viewpoint, distance, focus, light, and movement setup for a reason. Consecutive frontal masters made escalation feel static. Over-the-shoulders, reverse angles, details, low viewpoints, and spatial reveals can improve coverage while preserving the axis and geography.

**Physical direction needs landmarks.** Skiers/riders can appear to move uphill when prompts use only generic downhill language. Bind motion to the actual resort base, horizon, slope fall line, and camera side. Compare adjacent frames, not just one attractive image. Likewise, left arm, screen-left, anatomical left, and travel direction are different instructions.

## Constrained edits and QA

**Use the existing frame as composition master.** For a face-only, goggles-only, bandage-only, crowd, or signage correction, bind the exact current take plus the relevant identity/object reference. Describe the one requested change and preserve successful camera, pose, lighting, geography, and props. More prose isn't always better; concise role instructions can avoid competing interpretations.

**Preservation prompts are not proof.** Corrections have changed gaze, faces, wardrobe, crowd count, background, entrance doors, or crop despite explicit preservation text. Compare original and revision at useful resolution. Count people/objects, verify who holds each item, and check action state separately from photographic finish.

**Brand text requires actual supplied art.** Attach the full, sharp logo/packaging/prop source, not only its written name or a clipped crop. A visible reference attachment does not mean printed geometry or letters are correct. Generated end cards and tiny product marks need close review; final exact artwork may be better composited from the authorized original.

**Human activity needs individual jobs.** Background people rendered as a rigid audience when the brief only requested a crowd. Give distinct ordinary tasks, depth groups, varied facing directions, and believable setup/check-in behavior. Avoid rewriting an entire successful scene to fix one count or local pose.

**Batch completion is not creative completion.** A provider can finish every frame while several miss cast count, door positions, perspective, prop state, or exact text. Log concrete issues by take/shot. Targeted corrective runs must stay within the user's generation/retry scope; do not erase uncertainty with unbounded paid attempts.

## Source-video editing

**The source video and corrected still have different jobs.** Source video controls opening, camera, motion, original action/timing, background, light, blur, and grade. A corrected still can be appearance-only for a local part. Don't let it silently become the start frame or target pose. Reference-guided regeneration can interpret their difference as a transition instead of a constant edit.

**Native editing must actually be enabled.** Inspect the current model/schema for an explicit supported Edit mode, such as videoReferenceMode. A prompt saying EDIT MODE does not set it. Verify the actual source clip, mode and bindings; use supported UI when the required mode is absent from the structured interface.

**Minimum-duration padding is a scoped workaround.** If the user requests black padding to meet a live model's minimum, preserve the original action frames and timestamps, append black, and verify both frame count/rate and the hard cut. Don't replace fast source motion with a frozen tail or extend the action. Padding is input preparation, not a promise the model will preserve timing; review and trim the output as requested.

**Tiny persistent changes can favor compositing.** Repeated tests made a passive vehicle detail glow, fade in, drift, or alter the camera. After bounded failed attempts, state the observed failure and consider an authorized tracked composite on the original frames. This offers direct control of persistence, blur, perspective, and occlusion. It is a task-specific option, not a mandatory replacement for generation.

## Operational references

Use [CLI operations](cli-operations.md) for IDs, generation receipts and recovery; [Board operations](board-operations.md) for observed layout and UI failures; [Delivery](delivery.md) for measured exports, manifests and reversible naming.
