#include "HelloWorldSubsystem.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/GameViewportClient.h"
#include "Engine/World.h"
#include "UEGitWorkshopLog.h"
#include "Styling/CoreStyle.h"
#include "Fonts/SlateFontInfo.h"
#include "Widgets/SOverlay.h"
#include "Widgets/Text/STextBlock.h"
#include "Widgets/Layout/SBorder.h"

void UHelloWorldSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);

    if (UWorld* World = GetWorld())
    {
        HandleWorldInitialized(*World);
    }

    PostWorldInitHandle = FWorldDelegates::OnPostWorldInitialization.AddLambda(
        [this](UWorld* World, const UWorld::InitializationValues)
        {
            if (World)
            {
                HandleWorldInitialized(*World);
            }
        });
}

void UHelloWorldSubsystem::Deinitialize()
{
    RemoveHelloMessage();
    ClearWorldBindings();

    if (PostWorldInitHandle.IsValid())
    {
        FWorldDelegates::OnPostWorldInitialization.Remove(PostWorldInitHandle);
        PostWorldInitHandle = FDelegateHandle();
    }

    Super::Deinitialize();
}

void UHelloWorldSubsystem::RemoveHelloMessage()
{
    if (HelloMessageTimerHandle.IsValid())
    {
        if (UWorld* World = MessageWorld.Get())
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
    MessageWorld.Reset();
}

void UHelloWorldSubsystem::HandleWorldInitialized(UWorld& World)
{
    if (!World.IsGameWorld())
    {
        return;
    }

    if (UGameInstance* OwningInstance = GetGameInstance())
    {
        if (World.GetGameInstance() != OwningInstance)
        {
            return;
        }
    }

    ClearWorldBindings();
    PendingHelloWorld = &World;

    if (World.HasBegunPlay())
    {
        ShowHelloMessage(World);
        PendingHelloWorld.Reset();
        return;
    }

    WorldBeginPlayHandle = World.OnWorldBeginPlay.AddUObject(
        this,
        &UHelloWorldSubsystem::HandleWorldBeginPlay);
}

void UHelloWorldSubsystem::HandleWorldBeginPlay()
{
    if (UWorld* World = PendingHelloWorld.Get())
    {
        ShowHelloMessage(*World);

        if (WorldBeginPlayHandle.IsValid())
        {
            World->OnWorldBeginPlay.Remove(WorldBeginPlayHandle);
            WorldBeginPlayHandle = FDelegateHandle();
        }
    }

    PendingHelloWorld.Reset();
}

void UHelloWorldSubsystem::ShowHelloMessage(UWorld& World)
{
    if (!GEngine || !GEngine->GameViewport)
    {
        return;
    }

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

    World.GetTimerManager().SetTimer(
        HelloMessageTimerHandle,
        this,
        &UHelloWorldSubsystem::RemoveHelloMessage,
        5.0f,
        false);

    MessageWorld = &World;
}

void UHelloWorldSubsystem::ClearWorldBindings()
{
    if (PendingHelloWorld.IsValid() && WorldBeginPlayHandle.IsValid())
    {
        if (UWorld* World = PendingHelloWorld.Get())
        {
            World->OnWorldBeginPlay.Remove(WorldBeginPlayHandle);
        }
    }

    WorldBeginPlayHandle = FDelegateHandle();
    PendingHelloWorld.Reset();
}
