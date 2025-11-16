#include "HelloWorldSubsystem.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "UEGitWorkshopLog.h"
#include "Styling/CoreStyle.h"
#include "Styling/SlateFontInfo.h"
#include "Widgets/SOverlay.h"
#include "Widgets/Text/STextBlock.h"
#include "Widgets/Layout/SBorder.h"

void UHelloWorldSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);

    if (UWorld* World = GetWorld())
    {
        if (World->IsGameWorld() && GEngine && GEngine->GameViewport)
        {
            constexpr const TCHAR* HelloString = TEXT("Hello World");

            UE_LOG(LogUEGitWorkshop, Display, TEXT("%s"), HelloString);

            RemoveHelloMessage();

            const FText HelloText = FText::FromString(HelloString);
            const FSlateFontInfo FontInfo = FCoreStyle::GetDefaultFontStyle("Bold", 64);
            const FLinearColor TextColor(0.1f, 0.95f, 0.7f);

            HelloMessageWidget =
                SNew(SOverlay)
                + SOverlay::Slot()
                .HAlign(HAlign_Center)
                .VAlign(VAlign_Center)
                [
                    SNew(SBorder)
                    .Padding(FMargin(24.0f))
                    .BorderBackgroundColor(FLinearColor(0.f, 0.f, 0.f, 0.55f))
                    [
                        SNew(STextBlock)
                        .Justification(ETextJustify::Center)
                        .Font(FontInfo)
                        .ColorAndOpacity(TextColor)
                        .ShadowOffset(FVector2D(2.0f, 2.0f))
                        .ShadowColorAndOpacity(FLinearColor(0.f, 0.f, 0.f, 0.8f))
                        .Text(HelloText)
                    ]
                ];

            GEngine->GameViewport->AddViewportWidgetContent(HelloMessageWidget.ToSharedRef(), 100);

            World->GetTimerManager().SetTimer(
                HelloMessageTimerHandle,
                this,
                &UHelloWorldSubsystem::RemoveHelloMessage,
                5.0f,
                false
            );
        }
    }
}

void UHelloWorldSubsystem::Deinitialize()
{
    RemoveHelloMessage();
    Super::Deinitialize();
}

void UHelloWorldSubsystem::RemoveHelloMessage()
{
    if (HelloMessageTimerHandle.IsValid())
    {
        if (UWorld* World = GetWorld())
        {
            World->GetTimerManager().ClearTimer(HelloMessageTimerHandle);
        }
        HelloMessageTimerHandle.Invalidate();
    }

    if (HelloMessageWidget.IsValid() && GEngine && GEngine->GameViewport)
    {
        GEngine->GameViewport->RemoveViewportWidgetContent(HelloMessageWidget.ToSharedRef());
    }

    HelloMessageWidget.Reset();
}
